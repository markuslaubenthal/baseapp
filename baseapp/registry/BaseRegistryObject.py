from typing import TypeVar
from .Parameter import Parameter
import logging
from copy import copy

class BaseRegistryObject(object):
    """
    Base class for all registry objects.
    """
    name = "BaseRegistryObject"
    logger = logging.getLogger(__name__)
    timeout = 5
    _path = None
    
    DEBUG_MODE = False
    
    def __init__(self, name: str, description: str, id=None):
        """
        Constructor.
        """
        self.name = name
        self.description = description
        self.id = id
        self.logger = logging.getLogger(
            self.__class__.__module__ + "." + self.__class__.__name__ + "." + self.id)
        classMembers = dir(self.__class__)
        for member in classMembers:
            if issubclass(type(getattr(self.__class__, member)), Parameter):
                self.logger.debug("Copying parameter: %s", member)
                parameter = super().__getattribute__(member)
                super().__setattr__(member, copy(parameter))
                # super().__getattribute__(member).init()
        

    def __str__(self):
        """
        String representation.
        """
        return self.name

    def __repr__(self):
        """
        String representation.
        """
        return self.name

    def __eq__(self, other):
        """
        Equality operator.
        """
        return self.id == other.id

    def __ne__(self, other):
        """
        Inequality operator.
        """
        return self.id != other.id

    def __hash__(self):
        """
        Hash function.
        """
        return hash(self.id)

    def __cmp__(self, other):
        """
        Comparison operator.
        """
        return self.id == other.id

    def __lt__(self, other):
        """
        Less than operator.
        """
        return self.id < other.id

    def __le__(self, other):
        """
        Less than or equal to operator.
        """
        return self.id <= other.id

    def __gt__(self, other):
        """
        Greater than operator.
        """
        return self.id > other.id

    def __ge__(self, other):
        """
        Greater than or equal to operator.
        """
        return self.id >= other.id

    def get_id(self):
        """
        Get the id.
        """
        return self.id

    def get_name(self):
        """
        Get the name.
        """
        return self.name

    def get_description(self):
        """
        Get the description.
        """
        return self.description

    def set_id(self, id):
        """
        Set the id.
        """
        self.id = id

    def set_name(self, name):
        """
        Set the name.
        """
        self.name = name

    def set_description(self, description):
        """
        Set the description.
        """
        self.description = description
        
    def initParameters(self):
        classMembers = dir(self.__class__)
        for member in classMembers:
            if issubclass(type(getattr(self.__class__, member)), Parameter):
                self.logger.debug("Initializing parameter value: %s", member)
                super().__getattribute__(member).init()
    
    def setParameter(self, name, value):
        """
        Set parameter value.
        """
        self.logger.debug("Setting parameter: %s = %s", name, value)
        setattr(self, name, value)
    
    def setLogger(self, logger):
        self.logger = logger
    
    @classmethod
    def getParameters(cls):
        """
        Get parameters.
        """
        classMembers = dir(cls)
        parameters = []
        for member in classMembers:
            if issubclass(type(getattr(cls, member)), Parameter):
                parameters.append((member, getattr(cls, member)))
        return parameters
    
    def getParameterValues(self):
        """
        Get parameter values.
        """
        classMembers = dir(self.__class__)
        parameters = {}
        for member in classMembers:
            if issubclass(type(getattr(self.__class__, member)), Parameter):
                parameters[member] = getattr(self, member)
        return parameters
    
    def __setattr__(self, name, value):
        """
        Set attribute.
        """
        try:
            attribute = super().__getattribute__(name)
        except AttributeError:
            attribute = None
        if issubclass(type(attribute), Parameter):
            attribute.setValue(value)
        else:
            super().__setattr__(name, value)
    
    def __getattribute__(self, name):
        """
        Get attribute.
        """
        attribute = super().__getattribute__(name)
        if issubclass(type(attribute), Parameter):
            return attribute.value
        else:
            return attribute
    
    @classmethod
    def _setPath(cls, path):
        cls._path = path
        
        
TypeRegistryObject = TypeVar('TypeRegistryObject', bound=BaseRegistryObject)