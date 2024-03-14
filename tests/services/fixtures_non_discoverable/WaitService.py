from baseapp.registry.services import BaseService
from baseapp.registry import Parameter
import pytest
import time

class IndefiniteWaitService(BaseService):
    name = "WaitService"
    
    def run(self):
        self.logger.critical("WaitService is running")
        
        while True:
            time.sleep(1)
            
class StoppableWaitService(BaseService):
    name = "WaitService"
    
    def run(self):
        self.logger.critical("WaitService is running")
        
        while not self.stopEvent.is_set():
            time.sleep(1)
            
        self.logger.critical("WaitService exited")