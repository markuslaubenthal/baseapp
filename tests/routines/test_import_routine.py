import pytest
from typing import TypeVar, Generic, get_args

from baseapp.registry import Discovery
from baseapp.registry.routines import BaseRoutine
from baseapp.registry.services import BaseService
import logging

class TestImportRoutine:
    def test_import_routine_single_file(self, caplog):
        caplog.set_level(logging.DEBUG)
        # BaseRoutineDiscovery = Discovery[BaseRoutine]
        routine = Discovery[BaseRoutine]().import_routine("tests/routines/fixtures/MockRoutine.py")
        assert routine.name == "MockRoutine"
        assert routine.__doc__ == "This is a Mock Routine"
        
    def test_import_routine_does_not_allow_importing_non_routines(self):
        with pytest.raises(ImportError):
            Discovery[BaseRoutine]().import_routine("tests/routines/fixtures/ThisIsNotARoutineClass.py")
    
    @pytest.mark.parametrize(
        "BaseClass,names,base_path,num_classes",
        [
            (BaseRoutine, ["MockRoutine", "MockRoutine2"], "tests/routines/fixtures", 2),
            (BaseService, ["MockRoutine"], "tests/services/fixtures", 0)
        ]
    )
    def test_discovery_only_finds_specified_subclasses(self, BaseClass, names, base_path, num_classes):
        classes = Discovery[BaseClass]().discover("tests/routines/fixtures")
        assert len(classes) == num_classes
        for index, cls in enumerate(classes):
            assert issubclass(cls, BaseClass)
            assert(cls.name == names[index])