from baseapp.registry.routines import BaseRoutine
from baseapp.registry import Parameter
import pytest

class MockRoutine(BaseRoutine):
    """This is a Mock Routine"""
    
    name = "MockRoutine"
    
    mock_parameter = Parameter[str]("mock_parameter", default = "mock_value").env("MOCK_PARAMETER")
    a = Parameter[int]("a", default = 1).env("INT_A")
    b = Parameter[int]("b", default = 2).env("INT_B")
    result = Parameter[int]("result", default = None)
    
    def run(self):
        self.result = self.a + self.b
        print("Result is", self.result)
        print("DEBUG MODE", self.DEBUG_MODE)
        
@pytest.fixture
def mockRoutineProvider():
    def provide():
        mr = MockRoutine()
        mr.initParameters()
        return mr
    return provide