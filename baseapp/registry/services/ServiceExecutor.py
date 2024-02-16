from ..Executor import Executor
from .BaseService import BaseService

import logging
from threading import Thread, Event

class ServiceExecutor(Executor):
    
    def __init__(self, serviceClass: BaseService.__class__):
        super().__init__()
        self.serviceClass = serviceClass
        self.events = []
        self.state = None
        self.thread = None
        self.args = None
        self.kwargs = None
    
    def updateState(self, state):
        self.state = state
        
    def getCurrentState(self):
        return self.state
    
    def setArguments(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        
    def run(self):
        super().run()
        self.instance = self.serviceClass()
        self.instance.setExecutor(self)
        self.instance.setStopEvent(self.stopEvent)
        self.instance.setLogger(
            logging.getLogger(
                "baseapp.services.{}.{}".format(
                    self.instance.__class__.__name__,
                    id(self.instance))))
        
        for name, param in self.kwargs.items():
            self.instance.setParameter(name, param)
        
        self.thread = Thread(target=self.instance.__start__)
        self.thread.daemon = True
        self.thread.start()
        
        import time
        
        # TODO: Here we should start an event loop instead of sleeping
        while not self.stopEvent.is_set():
            time.sleep(1)
        self.logger.critical("Stop event set")
            
        self.logger.critical("Waiting for thread to join")
        self.thread.join(self.instance.timeout)
        self.logger.critical("Thread joined")
    
    def __loop__(self):
        while not self.stopEvent.is_set():
            pass

        