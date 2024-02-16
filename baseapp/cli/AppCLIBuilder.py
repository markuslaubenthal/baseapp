import click
import logging

class AppCLIBuilder:
    def __init__(self, app):
        self.app = app
        
    def build(self):
        @click.group()
        @click.option('--debug/--no-debug', default=False)
        def cli(debug):
            self.app.setLogLevel(logging.DEBUG if debug else logging.INFO)
            self.app.setDebug(debug)
            
        return cli