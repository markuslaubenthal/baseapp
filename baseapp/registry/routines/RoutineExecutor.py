from ..Executor import Executor
from .BaseRoutine import BaseRoutine
import logging
import time
import random

class RoutineExecutor(Executor):
    
    def __init__(self, routine: BaseRoutine.__class__):
        super().__init__()
        self.routine = routine
    
    def run(self, *args, **kwargs):
        super().run()
        instance_id = str(int(time.time())) + "-" + str(random.randint(0, 9999)).rjust(4, "0")
        routineInstance = self.routine(instance_id)
        for name, param in kwargs.items():
            routineInstance.setParameter(name, param)
        
        res = routineInstance.run()
        self.logger.debug("Result: %s", res)
        return res