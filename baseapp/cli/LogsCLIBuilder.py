import click
from ..registry import Registry
from ..registry.routines import BaseRoutine, RoutineExecutor
import re

pattern = re.compile(r'(?<!^)(?=[A-Z])')
def camel_to_snake(name):
    return pattern.sub('_', name).lower()

class LogsCLIBuilder:
    def __init__(self, app):
        self.app = app
    
    def build(self, group: "click.group"):
        
        @group.group(name="logs")
        def logs_group(**kwargs):
            pass
        
        @logs_group.command(name="prune")
        def logs_prune(**kwargs):
            # prune logs
            self.app.pruneLogFiles()
                    
        # logs_prune.add_command(cmd_wrapper(routine), name_camel_case)
        