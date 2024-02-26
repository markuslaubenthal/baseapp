import pytest
from baseapp import BaseApp

from .fixtures.ChildApp import childApp as app
from click.testing import CliRunner
from unittest import mock
import os
import logging
import random
import time

def get_log_file(file_name, log_directory):
    return os.path.join(log_directory, file_name)

class TestLogFiles:
    def test_create_log(self, app):
        assert isinstance(app, BaseApp)
        
        logger = logging.getLogger("baseapp")
        random_message = str(random.random()) + "." + str(time.time())
        logger.critical(random_message)
        assert os.path.exists("tests/logs/BaseApp.log")
        assert random_message in open("tests/logs/BaseApp.log").read()
        
    # TODO: Remove app from the fixture and use a new instance of BaseApp
    # This way we can actually use the log_destination from the environment variable
    # instead of fixing it in the fixture
    def test_prune_log_files(self, app):
        assert isinstance(app, BaseApp)
        
        logger_names = [("BaseApp.log", "baseapp"), ("routines.log", "baseapp.registry.routines"), ("services.log", "baseapp.registry.services")]
        log_directory = app.config["log_destination"]
        
        log_files = app.getLogFiles()
        assert len(log_files) == 3
        
        for file_name, logger_name in logger_names:
            logger = logging.getLogger(logger_name)
            random_message = str(random.random()) + "." + str(time.time())
            logger.critical(random_message)
            
            log_file = os.path.join(log_directory, file_name)
            assert os.path.exists(log_file)
            assert random_message in open(log_file).read()
            assert log_file in log_files

        app.pruneLogFiles()
        for file_name, logger_name in logger_names:
            log_file = os.path.join(log_directory, file_name)
            assert not os.path.exists(log_file)
        