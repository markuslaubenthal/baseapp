from enum import Enum


class ExecutorState(Enum):
    IDLE = -1
    INITIALIZING = 0
    INITIALIZED = 1
    STARTING = 2
    RUNNING = 3
    STOPPING = 4
    STOPPED = 5
    FINISHED = 6
    TERMINATED = 7
    SHUTTING_DOWN = 100