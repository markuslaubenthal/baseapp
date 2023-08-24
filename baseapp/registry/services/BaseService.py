import logging
from ..BaseRegistryObject import BaseRegistryObject

class BaseService(BaseRegistryObject):
    def __init__(self):
        super().__init__(self.name, self.__doc__)
    
    def run(self):
        pass