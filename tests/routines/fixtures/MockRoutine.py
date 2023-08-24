from baseapp.registry.routines import BaseRoutine
from baseapp.registry import Parameter
import pytest

class MockRoutine(BaseRoutine):
    """This is a Mock Routine"""
    
    name = "MockRoutine"
    
    mock_parameter = Parameter[str]("mock_parameter", default = "mock_value").env("MOCK_PARAMETER")
    a = Parameter[int]("a", default = 1).env("INT_A")
    b = Parameter[int]("b", default = 2).env("INT_B")
        
    def run(self):
        return self.a + self.b
        
@pytest.fixture
def mockRoutineProvider():
    def provide():
        mr = MockRoutine()
        mr.initParameters()
        return mr
    return provide