from typing import Generic
from .BaseRegistryObject import BaseRegistryObject, TypeRegistryObject

import logging

class Registry(Generic[TypeRegistryObject]):
    
    def __init__(self):
        self.elements = {}
    
    def register(self, el: TypeRegistryObject):
        self.elements[el.name] = el
        logging.info(f"Registered object {el.name}")
        
    def unregister(self, name):
        try:
            del self.elements[name]
        except KeyError as e:
            logging.warning("Could not unregister object {name}")
        
    def getRegistered(self):
        return self.elements.values()
        
    def get(self, name):
        try:
            return self.elements[name]
        except KeyError:
            raise KeyError(f"Object '{name}' not found in registry.")
        
    def __len__(self):
        return len(self.elements)