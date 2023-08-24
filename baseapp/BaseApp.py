from .registry import Discovery, Registry
from .registry.routines import BaseRoutine
from .registry.services import BaseService
from .cli import AppCLIBuilder, RoutinesCLIBuilder

import click
import dotenv
import logging
import sys

class BaseApp:
    def __init__(
            self,
            configFile = "config/conf.yaml",
            enableRoutineDiscovery = True,
            enableServiceDiscovery = True):
        
        self.enableRoutineDiscovery = enableRoutineDiscovery
        self.enableServiceDiscovery = enableServiceDiscovery
        self.routineRegistry = Registry[BaseRoutine]()
        self.serviceRegistry = Registry[BaseService]()
        self.configFile = configFile
        
        self.config = self.loadDefaultConfig()
        self.cli = None
        
        dotenv.load_dotenv(".env")

    
    def loadDefaultConfig(self):
        return {
            "routines_directories": ["routines"],
            "services_directories": ["services"]
        }
    
    def _discoverRoutines(self, directory):
        routines = Discovery[BaseRoutine]().discover(directory)
        for routine in routines:
            self.routineRegistry.register(routine)
            
    def _discoverServices(self, directory):
        services = Discovery[BaseService]().discover(directory)
        for service in services:
            self.serviceRegistry.register(service)
    
    def setLogLevel(self, level):
        logging.basicConfig(stream=sys.stdout, level=level)
    
    def init(self):
        if self.enableRoutineDiscovery:
            for directory in self.config["routines_directories"]:
                self._discoverRoutines(directory)
            
        if self.enableServiceDiscovery:
            for directory in self.config["services_directories"]:
                self._discoverServices(directory)
                
        self.cli = AppCLIBuilder(self).build()
        
        RoutinesCLIBuilder(self.routineRegistry).build(group=self.cli)
        
    def start(self, *args, **kwargs):
        self.init()
        self.run(*args, **kwargs)
        
    def run(self, *args, **kwargs):
        self.cli()