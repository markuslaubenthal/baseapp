from ..BaseRegistryObject import BaseRegistryObject
import logging

class BaseService(BaseRegistryObject):
    
    logger = logging.getLogger(__name__)
    
    def __init__(self):
        super().__init__(self.name, self.__doc__)
        self.executor = None
        self.stopEvent = None
        
    def setExecutor(self, executor):
        self.executor = executor
        
    def setStopEvent(self, stopEvent):
        self.stopEvent = stopEvent
        
    def __onstart__(self):
        self.executor.updateState("started")
        
    def __onstop__(self):
        self.executor.updateState("stopped")
        
    def __start__(self):
        self.logger.info("Starting service: %s", self.name)
        
        self.__onstart__()
        self.run()
        self.__onstop__()
        
    def __stop__(self):
        self.logger.info("Stopping service: %s", self.name)
        self.stopEvent.set()
    
    
    def stop(self):
        raise NotImplemented("stop method not implemented")
    
    def run(self):
        raise NotImplemented("run method not implemented")