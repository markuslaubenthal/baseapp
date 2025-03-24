from enum import Enum


class ExecutorState(Enum):
    IDLE = -1
    INITIALIZING = 0
    INITIALIZED = 1
    STARTING = 2
    RUNNING = 3
    STOPPING = 101
    SHUTTING_DOWN = 102
    STOPPED = 103
    FINISHED = 104
    TERMINATED = 105
    ERROR = 106