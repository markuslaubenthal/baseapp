from typing import Generic
from .BaseRegistryObject import BaseRegistryObject, TypeRegistryObject

import logging

class Registry(Generic[TypeRegistryObject]):
    logger = logging.getLogger("BaseApp")
    
    def __init__(self):
        self.elements = {}
        self.executors = []
    
    def register(self, el: TypeRegistryObject):
        self.elements[el.name] = el
        self.logger.info(f"Registered object {el.name}")
        
    def unregister(self, name):
        try:
            del self.elements[name]
        except KeyError as e:
            self.logger.warning("Could not unregister object {name}")
        
    def getRegistered(self):
        return self.elements.values()
        
    def get(self, name):
        try:
            return self.elements[name]
        except KeyError:
            raise KeyError(f"Object '{name}' not found in registry.")
        
    def __len__(self):
        return len(self.elements)
    
    def stopAll(self):
        for executor in self.executors:
            self.logger.info(f"Stopping executor {executor}")
            executor.stop()
    
    def registerExecutor(self, executor):
        self.logger.info(f"Adding executor {executor}")
        self.executors.append(executor)