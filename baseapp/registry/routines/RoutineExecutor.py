from ..Executor import Executor
from .BaseRoutine import BaseRoutine
import logging

class RoutineExecutor(Executor):
    
    def __init__(self, routine: BaseRoutine.__class__):
        super().__init__()
        self.routine = routine
    
    def run(self, *args, **kwargs):
        super().run()
        routineInstance = self.routine()
        for name, param in kwargs.items():
            routineInstance.setParameter(name, param)
        
        res = routineInstance.run()
        self.logger.debug("Result: %s", res)
        return res