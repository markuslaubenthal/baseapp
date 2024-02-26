import multiprocessing
multiprocessing.set_start_method('fork')
from .registry import Discovery, Registry
from .registry.routines import BaseRoutine
from .registry.services import BaseService
from .cli import AppCLIBuilder, RoutinesCLIBuilder, ServicesCLIBuilder, LogsCLIBuilder, LazyGroup
import click
import dotenv
import sys, os

import logging
from logging import FileHandler

import atexit


import pprint
class BaseApp:
    def __init__(
            self,
            configFile = "config/conf.yaml",
            enableRoutineDiscovery = True,
            enableServiceDiscovery = True):
        
        dotenv.load_dotenv(".env")
        
        # Logging stuff
        self.config = self.loadDefaultConfig()
        self.logFormat = self.config["log_format"]
        logging.basicConfig(
            format=self.logFormat,
            level=logging.getLevelName(self.config["log_level"])
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
        
        
        
        self.logger = logging.getLogger(__name__)
        
        self.setupLogger()
        self.setupExitHandler()
        
        
    
    def getLogFiles(self):
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
            "log_destination": "logs/",
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
        baseLogHandler = logging.FileHandler(baseLogFilename, mode='a', encoding=None, delay=False, errors=None)
        baseLogHandler.setFormatter(formatter)
        baseLogger.addHandler(baseLogHandler)
        
        serviceLogger = logging.getLogger("baseapp.registry.services")
        serviceLogHandler = logging.FileHandler(serviceLogFilename, mode='a', encoding=None, delay=False, errors=None)
        serviceLogHandler.setFormatter(formatter)
        serviceLogger.addHandler(serviceLogHandler)
        
        routineLogger = logging.getLogger("baseapp.registry.routines")
        routineLogHandler = logging.FileHandler(routineLogFilename, mode='a', encoding=None, delay=False, errors=None)
        routineLogHandler.setFormatter(formatter)
        routineLogger.addHandler(routineLogHandler)
    
    def _discoverRoutines(self, directory):
        routines = Discovery[BaseRoutine]().discover(directory)
        for routine in routines:
            self.routineRegistry.register(routine)
            
    def _discoverServices(self, directory):
        services = Discovery[BaseService]().discover(directory)
        for service in services:
            self.serviceRegistry.register(service)
    
    def setLogLevel(self, level):
        self.log_level = level
        root_logger = logging.getLogger()
        root_logger.setLevel(level)
    
    def discoverAll(self):
        if self.enableRoutineDiscovery:
            for directory in self.config["routines_directories"]:
                self._discoverRoutines(directory)
            
        if self.enableServiceDiscovery:
            for directory in self.config["services_directories"]:
                self._discoverServices(directory)
        
    def initCLI(self):
        self.logger.debug("Building CLI")
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
        for routine in self.routineRegistry.executors:
            # if the routine has not started, it will not join
            if routine.is_alive():
                routine.join()
        for service in self.serviceRegistry.executors:
            service.join()
    
    def stop(self):
        if self.isStopped:
            return
        self.isStopped = True
        self.logger.info("Stopping routines and services")
        self.routineRegistry.stopAll()
        self.serviceRegistry.stopAll()
        self.logger.info("Waiting for all processes to shutdown")
        self.waitForAll()
        
        self.logger.info("Everything shutdown")
        
        
        
    
    def run(self, *args, **kwargs):
        try:
            self.cli(standalone_mode=False)#, *args, **kwargs)
        except click.exceptions.Abort:
            self.logger.critical("KeyboardInterrupt")
        except click.exceptions.ClickException as e:
            e.show()