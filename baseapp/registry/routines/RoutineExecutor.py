from typing import Type

from baseapp.registry.routines import BaseRoutine
from baseapp.registry.Executor import Executor

class RoutineExecutor(Executor):
    
    def __init__(self, routine: Type[BaseRoutine]):
        super().__init__()
        self.routine = routine
    
    
    def run(self, *args, **kwargs):
        super().run()
        instance_id = self.createInstanceId()
        routineInstance = self.routine(instance_id)
        for name, param in kwargs.items():
            routineInstance.setParameter(name, param)
        
        res = routineInstance.run()
        self.logger.debug("Result: %s", res)
        return res