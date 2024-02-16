from baseapp.registry.services import BaseService

import time

class MockService(BaseService):
    name = "MockService"
    def __init__(self):
        pass
    
    def run(self):
        self.logger.critical("MockService is running")
        
        for i in range(3):
            time.sleep(1)
            if self.stopEvent.is_set():
                break
            
        self.logger.critical("MockService exited")