import pytest
from baseapp import BaseApp

from .fixtures.ChildApp import childApp as app
from click.testing import CliRunner
from unittest import mock
import os

class TestBaseApp:
    def test_baseapp(self, app):
        assert isinstance(app, BaseApp)
        
        assert app.enableRoutineDiscovery
        assert app.enableServiceDiscovery
        assert len(app.routineRegistry) == 2
        assert len(app.serviceRegistry) == 1
    
    @mock.patch.dict(os.environ, {"INT_A": "1", "INT_B": "2"})
    def test_cli(self, app):
        app.initCLI()
        assert app.cli is not None
        assert app.cli.name == "cli"
        
        runner = CliRunner()
        result = runner.invoke(app.cli, ['--debug', 'routines', 'run', 'mock_routine'], standalone_mode=False)
        assert result.exit_code == 0
        assert 'Result is 3' in result.output
        assert 'DEBUG MODE True' in result.output
        
        result = runner.invoke(app.cli, ['--no-debug', 'routines', 'run', 'mock_routine'], standalone_mode=False)
        assert result.exit_code == 0
        assert 'Result is 3' in result.output
        assert 'DEBUG MODE False' in result.output