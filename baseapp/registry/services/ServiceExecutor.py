from typing import Type
from threading import Thread

from baseapp.registry.Executor import Executor
from baseapp.registry.services import BaseService
from baseapp.registry.ExecutorState import ExecutorState

class ServiceExecutor(Executor):
    
    def __init__(self, serviceClass: Type[BaseService]):
        super().__init__()
        self.serviceClass = serviceClass
        self.events = []
        # self.state = None
        self.thread = None
        self.args = tuple()
        self.kwargs = {}

    
    def setArguments(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        
    def run(self):
        super().run()
        self.updateState(ExecutorState.STARTING)
        
        instance_id = self.createInstanceId()
        self.instance = self.serviceClass(id=instance_id)
        self.instance.setExecutor(self)
        self.instance.setStopEvent(self.stopEvent)
        
        for name, param in self.kwargs.items():
            self.instance.setParameter(name, param)
        
        if self.serviceClass.__start_in_main_thread__:
            self.updateState(ExecutorState.RUNNING)
            self.instance.__start__()
            self.updateState(ExecutorState.FINISHED)
            return
        else:
            self.thread = Thread(target=self.instance.__start__)
            self.thread.daemon = True
            self.thread.start()
            self.updateState(ExecutorState.RUNNING)
        
        
        # Check if thread is alive.
        # TODO: If more complex checks have to be made, this code should
        # be executed in a asynchronous manner
        
        # This can also be handled with proper locks, conditions or whatever
        shouldRun = True
        while shouldRun:
            if self.stopEvent.is_set():
                self.logger.debug("Stop event set")
                try:
                    # Try soft shutdown if stop method is implemented
                    self.instance.stop()
                except NotImplementedError:
                    self.logger.debug("Stop method not implemented")
                    
                shouldRun = False
                self.updateState(ExecutorState.SHUTTING_DOWN)
                break
            if not self.thread.is_alive():
                self.logger.debug("Thread finished running")
                shouldRun = False
                self.updateState(ExecutorState.FINISHED)
                break
            self.thread.join(1)
            
        self.logger.debug("Stop event set")
        
        self.logger.debug("Waiting for thread to join")
        self.thread.join(self.instance.timeout)
        
        if self.thread.is_alive():
            # Terminate thread if it is still alive
            self.logger.debug("Thread still alive. Terminating")
            self.updateState(ExecutorState.TERMINATED)
            
            import os, signal
            pid = os.getpid()
            os.kill(pid, signal.SIGTERM)
            return
            
        self.logger.debug("Thread stopped successfully")
        
        if self.getCurrentState() == ExecutorState.SHUTTING_DOWN:
            self.updateState(ExecutorState.STOPPED)
    
    def __loop__(self):
        while not self.stopEvent.is_set():
            pass

        