from typing import Generic, TypeVar, get_args
import os
T = TypeVar("T")

class Parameter(Generic[T]):
    def __init__(self, name = None, description: str = None, default = None, required = False):
        self.name = name
        self.default = default
        self.value: T = default
        self.description = description
        
        self.from_env = False
        self.environment_variable_name = None
        self._required = required
        
        self.override = False
        self.override_value: T = None
        
    def env(self, name: str):
        """Gets the value of the parameter from the environment variable with the given name.

        Args:
            name (str): environment variable name
        """
        self.from_env = True
        self.environment_variable_name = name
        self.init()
        return self
    
    def init(self):
        if not self.override:
            if self.environment_variable_name is not None:
                self.value = os.getenv(self.environment_variable_name, self.default)
            else:
                self.value = self.default
        else:
            self.value = self.override_value
            
        self.value = self.cast(self.value)
        
    def setValue(self, value: T):
        self.override = True
        self.override_value = value
        self.init()
        
    def __getattribute__(self, name):
        if name == "value":
            return super().__getattribute__(name)
        else:
            return super().__getattribute__(name)
    
    @property
    def type(self):
        return get_args(self.__orig_class__)[0]
    
    @property
    def required(self):
        return self._required
    
    def cast(self, value: T):
        baseClass = get_args(self.__orig_class__)[0]
        if isinstance(value, baseClass):
            return value
        else:
            try:
                return baseClass(value)
            except:
                return value