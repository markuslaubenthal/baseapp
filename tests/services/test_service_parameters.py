import pytest
import os
from .fixtures.MockService import MockService, mockServiceProvider
from unittest import mock

class TestRoutineParameters:
    
    @mock.patch.dict(os.environ, {"MOCK_PARAMETER": "This comes from the environment"})
    def test_parameter_value_isset(self, mockServiceProvider):
        mockService = mockServiceProvider()
        assert mockService.mock_parameter == "This comes from the environment"
    
    @mock.patch.dict(os.environ, {"INT_A": "8", "INT_B": "9"})
    def test_overriding_parameter_value(self, mockServiceProvider):
        mockService = mockServiceProvider()
        assert mockService.a == 8
        assert mockService.b == 9
        
        
        mockService.setParameter("a", 3)
        mockService.setParameter("b", 4)
        
        assert mockService.a == 3
        assert mockService.b == 4
        
        mockService.a = 5
        mockService.b = 6
        
        assert mockService.a == 5
        assert mockService.b == 6
        
    @mock.patch.dict(os.environ, {"INT_A": "1", "INT_B": "2"})
    def test_overriden_parameter_value_is_not_reset(self, mockServiceProvider):
        mockService = mockServiceProvider()
        assert mockService.a == 1
        assert mockService.b == 2
        
        os.environ
        
        os.environ["INT_A"] = "3"
        os.environ["INT_B"] = "4"
        
        mockService.initParameters()
        
        assert mockService.a == 3
        assert mockService.b == 4
        
        
        # Override Values
        mockService.a = 5
        mockService.b = 6
        
        assert mockService.a == 5
        assert mockService.b == 6
        
        # Reinitialize with default values if not overriden
        mockService.initParameters()
        
        assert mockService.a == 5
        assert mockService.b == 6
    
    @mock.patch.dict(os.environ, {"INT_A": "8", "INT_B": "9"})
    def test_parameter(self):
        from baseapp.registry import Parameter
        a = Parameter[int]("a", "This is a parameter", default = 1).env("INT_A")
        a.init()
        assert a.value == 8