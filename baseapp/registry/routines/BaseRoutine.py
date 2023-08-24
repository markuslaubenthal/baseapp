import logging
from ..BaseRegistryObject import BaseRegistryObject

class BaseRoutine(BaseRegistryObject):
    name = "BaseRoutine"
    
    def __init__(self):
        super().__init__(self.name, self.__doc__)
    
    
    def run(self):
        raise NotImplemented("run method not implemented")