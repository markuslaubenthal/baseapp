import click
import logging

class AppCLIBuilder:
    def __init__(self, app):
        self.app = app
        
    def build(self):
        @click.group()
        @click.option('--debug/--no-debug', default=False)
        def cli(debug):
            pass
            
        return cli