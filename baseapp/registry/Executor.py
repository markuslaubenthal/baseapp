from multiprocessing import Process, Event, Value
import logging
import signal
import ctypes
import random
import time

from baseapp.registry.ExecutorState import ExecutorState

class Executor:
    def __init__(self):
        self.instance = None
        self.stopEvent = Event()
        self.logger = logging.getLogger(__name__)
        self.ignore_interrupt = False
        self.state = Value(ctypes.c_int8, ExecutorState.IDLE.value)

    def createInstanceId(self):
        return str(int(time.time())) + "-" + str(random.randint(0, 9999)).rjust(4, "0")
    
    def updateState(self, state: ExecutorState):
        self.state.value = state.value
    
    def setIgnoreInterrupt(self, ignore: bool):
        self.ignore_interrupt = ignore
    
    def getCurrentState(self):
        return ExecutorState(self.state.value)
    
    def run(self):
        # Ignore SIGINT
        
        # My Thoughts: This prevents the process from being killed by the parent process # Fact
        # By preventing the process from being killed, the parent process can't kill the child process
        # This is useful when the child process is a daemon process
        # We have to figure out if we want to keep this or not.
        # Option 1 is to keep the line and send stopevents and join the process for a graceful shutdown
        # Option 2 is to remove the line and let the process be killed forcefully by the parent
        # Further thoughts: This is only useful if the Executor is a process that was run by executor.start()
        # If the run method is invoked in the same process, this will just result in the program not being able
        # to exit with a keyboard interrupt
        if self.ignore_interrupt:
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            
        # TODO: Maybe for every executor have its own signal handler, such that it is not dependent
        # on the main App Process to send the stop signal to the executor.
    
    def stop(self):
        self.stopEvent.set()
        signal.signal(signal.SIGINT, signal.SIG_DFL)