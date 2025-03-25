import logging
from baseapp.logger.ColorCodes import Codes as CC, HelperCodes, TextColorCodes as TCC

# This is just for testing purposes
# The actual logger should be defined as the root logger and handle all logs for a specific child process
# This is just a simple logger that can be used to log from the routines and services directly

disableLogFiles = False

def create(
        programName: str,
        loggerName: str,
        color: CC = TCC.WHITE,
        logFormat: str = '%(asctime)s [%(levelname)s] [%(name)s] %(message)s',
        fileName: str = 'logs/{name}.log',
    ):
    
    colorFormatter = logging.Formatter(f"{color.value}{logFormat}{HelperCodes.RESET.value}")
    formatter = logging.Formatter(logFormat)
    logger = logging.getLogger(loggerName)
    logger.handlers.clear()
    std_handler = logging.StreamHandler()
    std_handler.setFormatter(colorFormatter)
    logger.addHandler(std_handler)
    
    if fileName is not None and not disableLogFiles:
        fileName = fileName.format(name=programName)
        fileHandler = logging.FileHandler(fileName, mode='a', encoding=None, delay=False)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)
    logger.propagate = False
    return logger