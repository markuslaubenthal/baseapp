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
        if value:
            click.echo("Operating in debug mode")
    
    def setLogLevel(self, ctx, param, logLevel: str | int):
        if isinstance(logLevel, str):
            level = logging.getLevelNamesMapping()[logLevel.upper()]
        if logLevel is not None:
            if self.app.debug:
                self.app.logger.warning("Log level cannot be set in debug mode")
                return
            level = logging.getLevelName(logLevel)
            self.app.setLogLevel(level)
            self.app.logger.debug(f"Log level set to {logLevel}")
    
    def build(self):
        # @click.group()
        @shell(prompt=f'{self.app.getApplicationName()}> ')
        @click.option('--debug/--no-debug', is_flag=True, callback=self.setDebug,
            expose_value=False, is_eager=True)
        @click.option('--log-level', expose_value=False, is_eager=True, callback=self.setLogLevel,
            type=click.Choice(['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'], case_sensitive=False))
        def cli():
            self.app.discoverAll()
            
        return cli