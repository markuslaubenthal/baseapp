import pytest
from baseapp import BaseApp

from .fixtures.ChildApp import childApp as app
from click.testing import CliRunner

class TestBaseApp:
    def test_baseapp(self, app):
        assert isinstance(app, BaseApp)
        
        assert app.enableRoutineDiscovery
        assert app.enableServiceDiscovery
        assert len(app.routineRegistry) == 2
        assert len(app.serviceRegistry) == 1
        
    def test_cli(self, app):
        assert app.cli is not None
        assert app.cli.name == "cli"
        
        runner = CliRunner()
        result = runner.invoke(app.cli, ['--debug', 'mock_routine'], standalone_mode=False)
        import logging
        assert result.return_value == 3
        assert result.exit_code == 0
        
        # assert len(app.cli.commands) == 2
        # assert "routine" in app.cli.commands
        # assert "service" in app.cli.commands