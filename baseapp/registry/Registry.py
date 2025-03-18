import logging
from typing import Generic

from baseapp.registry.BaseRegistryObject import TypeRegistryObject

class Registry(Generic[TypeRegistryObject]):
    logger = logging.getLogger(__name__)
    
    def __init__(self):
        self.elements = {}
        self.executors = []
    
    def register(self, el: TypeRegistryObject):
        self.elements[el.name] = el
        self.logger.debug(f"Registered object {el.name}")
        
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
        for executor, process in self.executors:
            if process is not None:
                self.logger.debug(f"Stopping executor {executor}")
                executor.stop()
        # for executor, process in self.executors:
        #     if process is not None:
        #         self.logger.debug(f"Joining executor {executor}")
        #         process.join(timeout = executor.instance.timeout)
        #         if process.is_alive():
        #             executor.updateState(ExecutorState.FAILED)
        #             process.terminate()
                
    def registerExecutor(self, executor):
        self.logger.debug(f"Adding executor {executor}")
        self.executors.append(executor)