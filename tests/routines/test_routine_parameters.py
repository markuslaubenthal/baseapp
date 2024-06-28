import pytest
import os
from unittest import mock
from .fixtures.MockRoutine import mockRoutineProvider, MockRoutine
from baseapp.registry import Parameter

class TestRoutineParameters:
    
    @mock.patch.dict(os.environ, {"MOCK_PARAMETER": "This comes from the environment"})
    def test_parameter_value_isset(self, mockRoutineProvider):
        mockRoutine = mockRoutineProvider()
        assert mockRoutine.mock_parameter == "This comes from the environment"
    
    @mock.patch.dict(os.environ, {"INT_A": "8", "INT_B": "9"})
    def test_overriding_parameter_value(self, mockRoutineProvider):
        mockRoutine = mockRoutineProvider()
        assert mockRoutine.a == 8
        assert mockRoutine.b == 9
        
        
        mockRoutine.setParameter("a", 3)
        mockRoutine.setParameter("b", 4)
        
        assert mockRoutine.a == 3
        assert mockRoutine.b == 4
        
        mockRoutine.a = 5
        mockRoutine.b = 6
        
        assert mockRoutine.a == 5
        assert mockRoutine.b == 6
        
        assert type(mockRoutine.a) == int
        assert type(mockRoutine.b) == int
        assert type(object.__getattribute__(mockRoutine, "a")) == Parameter
        assert type(object.__getattribute__(mockRoutine, "b")) == Parameter
        
    @mock.patch.dict(os.environ, {"INT_A": "1", "INT_B": "2"})
    def test_overriden_parameter_value_is_not_reset(self, mockRoutineProvider):
        mockRoutine = mockRoutineProvider()
        assert mockRoutine.a == 1
        assert mockRoutine.b == 2
        
        os.environ
        
        os.environ["INT_A"] = "3"
        os.environ["INT_B"] = "4"
        
        mockRoutine.initParameters()
        
        assert mockRoutine.a == 3
        assert mockRoutine.b == 4
        
        
        # Override Values
        mockRoutine.a = 5
        mockRoutine.b = 6
        
        assert mockRoutine.a == 5
        assert mockRoutine.b == 6
        
        # Reinitialize with default values if not overriden
        mockRoutine.initParameters()
        
        assert mockRoutine.a == 5
        assert mockRoutine.b == 6
    
    @mock.patch.dict(os.environ, {"INT_A": "8", "INT_B": "9"})
    def test_parameter(self):
        from baseapp.registry import Parameter
        a = Parameter[int]("a", "This is a parameter", default = 1).env("INT_A")
        a.init()
        assert a.value == 8
        
    @mock.patch.dict(os.environ, {"INT_A": "1", "INT_B": "2"})
    def test_extra_kwargs(self, mockRoutineProvider):
        mockRoutine = mockRoutineProvider()
        mockRoutine.setParameter("non_existent", 3)
        with pytest.raises(AttributeError):
            mockRoutine.non_existent
        assert mockRoutine.kwargs["non_existent"] == 3
        
        mockRoutine.another_one = 4
        assert mockRoutine.another_one == 4
        with pytest.raises(KeyError):
            mockRoutine.kwargs["another_one"]