from ..Executor import Executor
from .BaseRoutine import BaseRoutine
import logging

class RoutineExecutor(Executor):
    
    def __init__(self, routine: BaseRoutine.__class__):
        self.routine = routine
    
    def run(self, *args, **kwargs):
        print(args, kwargs)
        routineInstance = self.routine()
        
        for name, param in kwargs.items():
            routineInstance.setParameter(name, param)
        
        res = routineInstance.run()
        logging.info("Result: %s", res)
        return res