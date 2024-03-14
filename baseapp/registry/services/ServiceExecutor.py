from ..Executor import Executor
from .BaseService import BaseService

import logging
from threading import Thread
from multiprocessing import Value, Event
import ctypes
from ..ExecutorState import ExecutorState
import time

class ServiceExecutor(Executor):
    
    def __init__(self, serviceClass: BaseService.__class__):
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
        
        self.instance = self.serviceClass()
        self.instance.setExecutor(self)
        self.instance.setStopEvent(self.stopEvent)
        
        for name, param in self.kwargs.items():
            self.instance.setParameter(name, param)
        
        self.thread = Thread(target=self.instance.__start__)
        self.thread.daemon = True
        self.thread.start()
        self.updateState(ExecutorState.RUNNING)
        
        
        # Check if thread is alive.
        # TODO: If more complex checks have to be made, this code should
        # be executed in a asynchronous manner
        shouldRun = True
        while shouldRun:
            if self.stopEvent.is_set():
                self.logger.debug("Stop event set")
                try:
                    # Try soft shutdown if stop method is implemented
                    x = 0
                    # self.instance.stop()
                except NotImplemented:
                    self.logger.debug("Stop method not implemented")
                    
                shouldRun = False
                self.updateState(ExecutorState.SHUTTING_DOWN)
                break
            if not self.thread.is_alive():
                self.logger.info("Thread finished running")
                shouldRun = False
                self.updateState(ExecutorState.FINISHED)
                break
            self.thread.join(1)
            
        self.logger.debug("Stop event set")
            
        self.logger.debug("Waiting for thread to join")
        self.thread.join(self.instance.timeout)
        print("Thread joined")
        
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

        