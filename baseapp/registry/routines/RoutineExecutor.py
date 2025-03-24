from typing import Type

from baseapp.registry.routines import BaseRoutine
from baseapp.registry.Executor import Executor
from baseapp.registry.ExecutorState import ExecutorState

class RoutineExecutor(Executor):
    
    def __init__(self, routine: Type[BaseRoutine]):
        super().__init__()
        self.routine = routine
    
    
    def run(self, *args, **kwargs):
        super().run()
        self.updateState(ExecutorState.STARTING)
        instance_id = self.createInstanceId()
        routineInstance = self.routine(instance_id)
        for name, param in kwargs.items():
            routineInstance.setParameter(name, param)
        
        self.updateState(ExecutorState.RUNNING)
        try:
            res = routineInstance.run()
        except Exception as e:
            self.logger.error("An error occured while running the routine")
            self.logger.exception(e)
            self.updateState(ExecutorState.ERROR)
        else:
            self.updateState(ExecutorState.FINISHED)
            
        self.logger.debug("Result: %s", res)
        return res