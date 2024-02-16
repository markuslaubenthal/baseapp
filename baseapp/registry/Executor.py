from multiprocessing import Process, Event
import logging
import signal

class Executor(Process):
    def __init__(self):
        super().__init__()
        self.instance = None
        self.stopEvent = Event()
        self.logger = logging.getLogger(__name__)
        
    def run(self):
        # Ignore SIGINT
        # TODO: Find out why I did this
        return
        # My Thoughts: This prevents the process from being killed by the parent process # Fact
        # By preventing the process from being killed, the parent process can't kill the child process
        # This is useful when the child process is a daemon process
        # We have to figure out if we want to keep this or not.
        # Option 1 is to keep the line and send stopevents and join the process for a graceful shutdown
        # Option 2 is to remove the line and let the process be killed forcefully by the parent
        # Further thoughts: This is only useful if the Executor is a process that was run by executor.start()
        # If the run method is invoked in the same process, this will just result in the program not being able
        # to exit with a keyboard interrupt
        signal.signal(signal.SIGINT, signal.SIG_IGN)
    
    def stop(self):
        self.stopEvent.set()
        
        
# class Executor:
#     def __init__(self) -> None:
#         self.instance = None
#         self.stopEvent = Event()
#         self.logger = logging.getLogger("baseapp.Executor")
        
#     def run(self):
#         pass
    
#     def stop(self):
#         self.stopEvent.set()
    
#     # TODO: Fix this
#     def join(self):
#         return True