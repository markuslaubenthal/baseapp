import logging
from ..BaseRegistryObject import BaseRegistryObject

class BaseRoutine(BaseRegistryObject):
    name = "BaseRoutine"
    logger = logging.getLogger(__name__)
    logger_name = __name__
    def __init__(self, id=None):
        super().__init__(self.name, self.__doc__, id=id)
        
    
    def run(self):
        raise NotImplemented("run method not implemented")