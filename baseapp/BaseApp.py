import multiprocessing
import time

try:
    # TODO: Give a warning.
    # TODO: Change the routines and services such that they work with fork and spawn
    multiprocessing.set_start_method('fork')
except:
    pass

import logging
import click
import dotenv
import os
import atexit

from baseapp.cli import AppCLIBuilder, RoutinesCLIBuilder, ServicesCLIBuilder, LogsCLIBuilder
from baseapp.registry import Discovery, Registry
from baseapp.registry.routines import BaseRoutine
from baseapp.registry.services import BaseService

import pprint
class BaseApp:
    def __init__(
            self,
            applicationName = "BaseApp",
            configFile = "config/conf.yaml", # Not yet supported
            enableRoutineDiscovery = True,
            enableServiceDiscovery = True,
            discoverRecursive = False,
            logDestination = None,
            disableLogFiles = False,
        ):
        
        dotenv.load_dotenv(".env")
        self.discoverRecursive = discoverRecursive
        # Logging stuff
        self.disableLogFiles = disableLogFiles
        
        
        self.config = self.loadDefaultConfig()
        if logDestination is not None:
            self.config["log_destination"] = logDestination
        
        from baseapp.logger import Logger
        Logger.disableLogFiles = disableLogFiles
        Logger.logDestination = self.config["log_destination"]
            
        self.logFormat = self.config["log_format"]
        
        logLevel = self.config["log_level"]
        if isinstance(logLevel, str):
            logLevel = logging.getLevelNamesMapping()[logLevel.upper()]
        logging.basicConfig(
            format=self.logFormat,
            level=logging.getLevelName(logLevel)
        )
        
        self.pp = pprint.PrettyPrinter(indent=4)
        self.enableRoutineDiscovery = enableRoutineDiscovery
        self.enableServiceDiscovery = enableServiceDiscovery
        self.routineRegistry = Registry[BaseRoutine]()
        self.serviceRegistry = Registry[BaseService]()
        self.configFile = configFile
        
        self.cli = None
        self.debug = False
        
        self.isStopped = False
        
        self.setApplicationName(applicationName)
        
        self.logger = logging.getLogger(__name__)
        
        if not self.disableLogFiles:
            self.setupLogger()
        self.setupExitHandler()
    
    # TODO: Remove this function and put it somewhere else
    def pruneLogFiles(self):
        log_files = self.getLogFiles()
        for file in log_files:
            os.remove(file)
    
    def setApplicationName(self, applicationName):
        self.applicationName = applicationName
        
    def getApplicationName(self):
        return self.applicationName
    
    def getLogFiles(self):
        log_files = os.listdir(self.config["log_destination"])
        log_files = [os.path.join(self.config["log_destination"], file) for file in log_files]
        return log_files
        # return self.logFiles
    
    def setupExitHandler(self):
        def exitHandler():
            self.stop()
            
        atexit.register(exitHandler)
    
    def loadDefaultConfig(self):
        return {
            "routines_directories": ["routines"],
            "services_directories": ["services"],
            "log_destination": os.environ.get("LOG_DESTINATION") or "logs/",
            "log_level": "ERROR",
            "log_format": '%(asctime)s [%(levelname)s] [%(name)s] %(message)s'
        }
        
    def setupLogger(self):
        
        baseLogger = logging.getLogger("baseapp")
        logDestination = self.config["log_destination"]
        baseLogFilename = os.path.join(logDestination, "BaseApp.log")
        serviceLogFilename = os.path.join(logDestination, "services.log")
        routineLogFilename = os.path.join(logDestination, "routines.log")
        os.makedirs(logDestination, exist_ok=True)
        
        formatter = logging.Formatter(self.logFormat)
        baseLogHandler = logging.FileHandler(baseLogFilename, mode='a', encoding=None, delay=False)
        baseLogHandler.setFormatter(formatter)
        baseLogger.addHandler(baseLogHandler)
        
        serviceLogger = logging.getLogger("baseapp.registry.services")
        serviceLogHandler = logging.FileHandler(serviceLogFilename, mode='a', encoding=None, delay=False)
        serviceLogHandler.setFormatter(formatter)
        serviceLogger.addHandler(serviceLogHandler)
        
        routineLogger = logging.getLogger("baseapp.registry.routines")
        routineLogHandler = logging.FileHandler(routineLogFilename, mode='a', encoding=None, delay=False)
        routineLogHandler.setFormatter(formatter)
        routineLogger.addHandler(routineLogHandler)
    
    def _discoverRoutines(self, directory, recursive=False):
        routines = Discovery[BaseRoutine]().discover(directory, recursive=recursive)
        for routine in routines:
            self.routineRegistry.register(routine)
            
    def _discoverServices(self, directory, recursive=False):
        services = Discovery[BaseService]().discover(directory, recursive=recursive)
        for service in services:
            self.serviceRegistry.register(service)
    
    def setLogLevel(self, level: str | int):
        self.log_level = level
        root_logger = logging.getLogger()
        root_logger.setLevel(level)
    
    def discoverAll(self):
        if self.enableRoutineDiscovery:
            for directory in self.config["routines_directories"]:
                self._discoverRoutines(directory, recursive=self.discoverRecursive)
            
        if self.enableServiceDiscovery:
            for directory in self.config["services_directories"]:
                self._discoverServices(directory, recursive=self.discoverRecursive)
        
    def initCLI(self):
        self.cli = AppCLIBuilder(self).build()
        cli = self.cli
        RoutinesCLIBuilder(self.routineRegistry).buildLazy(group=self.cli)
        ServicesCLIBuilder(self.serviceRegistry).buildLazy(group=self.cli)
        LogsCLIBuilder(self).build(group=cli)
        
    
    def setDebug(self, debug):
        self.debug = debug
        BaseRoutine.DEBUG_MODE = debug
        BaseService.DEBUG_MODE = debug
        if debug:
            self.setLogLevel(logging.DEBUG)
    
    def start(self, *args, **kwargs):
        self.initCLI(*args, **kwargs)
        self.run(*args, **kwargs)
        self.stop()
    
    def waitForAll(self):
        for routine, process in self.routineRegistry.executors:
            if process is not None:
            # if the routine has not started, it will not join
                if process.is_alive():
                    process.join()
        for service, process in self.serviceRegistry.executors:
            if process is not None:
                if process.is_alive():
                    process.join()
    
    def onShellExit(self, ctx):
        self.stop()
    
    def stop(self):
        if self.isStopped:
            return
        self.isStopped = True
        self.logger.info("Stopping routines and services")
        self.routineRegistry.stopAll()
        self.serviceRegistry.stopAll()
        self.logger.debug("Waiting for all processes to shutdown")
        self.waitForAll()
        self.logger.debug("Everything shutdown")
        
    def run(self, *args, **kwargs):
        try:
            try:
                self.cli(standalone_mode=False)#, *args, **kwargs)
            except click.exceptions.Abort as e:
                raise KeyboardInterrupt()
            except click.exceptions.ClickException as e:
                e.show()
            
            running = True
            # This loop should probably by async and/or handled with events
            while running:
                executorStates = [executor.getCurrentState().value < 100 for executor, process in self.routineRegistry.executors]
                executorStates += [executor.getCurrentState().value < 100 for executor, process in self.serviceRegistry.executors]
                running = any(executorStates)
                if not running:
                    break
                time.sleep(0.5)
                
            self.waitForAll()
        except KeyboardInterrupt:
            self.logger.critical("KeyboardInterrupt")
            self.stop()
        self.waitForAll()