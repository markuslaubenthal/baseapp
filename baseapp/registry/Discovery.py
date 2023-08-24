import importlib.util
import inspect
import logging
import os
import sys
from typing import Generic, List, TypeVar, get_args, get_origin

BaseClass = TypeVar("BaseClass")

class Discovery(Generic[BaseClass]):
    """Discovers Routines in the routine folder of the app."""
    
    def discover(self, base_path) -> List[BaseClass]:
        """
        Discover routines and import them. A routine is a directory or file in the routines folder.
        If a directory is found, it is assumed that it has a __init__.py file that imports the extended BaseClass class.
        If a file is found, it is assumed to be a routine and is imported.
        """
        routines: List[BaseClass] = self.find_routines(base_path)
        return routines
    
    def import_routine(self, path, className = None) -> BaseClass:
        """
        Imports a routine from the given path.
        """
        
        baseClass = get_args(self.__orig_class__)[0]
        
        logging.info(f"Importing module {path}")
        module_name = ".".join(path.replace("/", ".").split(".")[0:-1])
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        
        if className is None:
            className = os.path.basename(path).split(".")[0]
        
        try:
            routine: BaseClass = getattr(module, className)
            assert issubclass(routine, baseClass), f"Routine {path} is not a subclass of BaseClass"
            return routine
        except Exception as e:
            raise ImportError(f"Could not import routine {className} from {path}") from e
    
    def get_routines_from_module(self, module) -> bool:
        """
        returns all routines in the given module.
        """
        baseClass = get_args(self.__orig_class__)[0]
        routines = []
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, baseClass) and obj is not baseClass:
                routines.append(obj)
        return routines
    
    def find_routines(self, path, recursive=False) -> List[str]:
        """
        Finds all routines in the given path.
        """
        
        routines = []
        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            
            if recursive and os.path.isdir(full_path):
                routines += self.find_routines(full_path, recursive=recursive)
            elif file.endswith(".py"):
                try:
                    module_name = ".".join(path.replace("/", ".").split(".")[0:-1])
                    spec = importlib.util.spec_from_file_location(module_name, full_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    routines += self.get_routines_from_module(module)
                
                except Exception as e:
                    raise e
                    logging.error("Could not import routines from %s", full_path)
                
                
        logging.info(f"Found {len(routines)} routines in path {path}")
        return routines