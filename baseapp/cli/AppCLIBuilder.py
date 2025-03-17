import click
import logging
from click_shell import shell

class AppCLIBuilder:
    def __init__(self, app):
        self.app = app
    
    def setDebug(self, ctx, param, value):
        if value:
            self.app.setLogLevel(logging.DEBUG)
        self.app.setDebug(value)
        click.echo("Operating in debug mode" if value else "")
    
    def setLogLevel(self, ctx, param, value):
        if value is not None:
            if self.app.debug:
                self.app.logger.warning("Log level cannot be set in debug mode")
                return
            level = logging.getLevelName(value)
            self.app.setLogLevel(level)
            self.app.logger.debug(f"Log level set to {value}")
    
    def build(self):
        # @click.group()
        @shell(prompt='baseapp> ')
        @click.option('--debug/--no-debug', is_flag=True, callback=self.setDebug,
            expose_value=False, is_eager=True)
        @click.option('--log-level', expose_value=False, is_eager=True, callback=self.setLogLevel,
            type=click.Choice(['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'], case_sensitive=False))
        def cli():
            self.app.discoverAll()
            
        return cli