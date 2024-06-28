from baseapp.registry.routines import BaseRoutine
from baseapp.registry import Parameter
import pytest

class TempRoutine(BaseRoutine):
    """This is a Mock Routine"""
    
    name = "TempRoutine"
    
    mock_parameter = Parameter[str]("mock_parameter", default = "mock_value").env("MOCK_PARAMETER")
    a = Parameter[int]("a", default = 1).env("INT_A")
    b = Parameter[int]("b", default = 2).env("INT_B")
    camelCase = Parameter[str](default = "camelCase").env("CAMEL_CASE")
    result = Parameter[int]("result", default = None)
    
    def run(self):
        print(self.camelCase)