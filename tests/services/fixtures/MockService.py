from baseapp.registry.services import BaseService
from baseapp.registry import Parameter
import pytest
import time

class MockService(BaseService):
    name = "MockService"
    
    mock_parameter = Parameter[str]("mock_parameter", default = "mock_value").env("MOCK_PARAMETER")
    a = Parameter[int]("a", default = 1).env("INT_A")
    b = Parameter[int]("b", default = 2).env("INT_B")
    result = Parameter[int]("result", default = None)
    
    def run(self):
        print("NEVER EXECUTED")
        self.logger.critical("MockService is running")
        
        for i in range(3):
            time.sleep(1)
            if self.stopEvent.is_set():
                break
            
        self.logger.critical("MockService exited")
        
@pytest.fixture
def mockServiceProvider():
    def provide():
        mr = MockService()
        mr.initParameters()
        return mr
    return provide