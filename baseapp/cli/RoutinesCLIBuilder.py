import click
from ..registry import Registry
from ..registry.routines import BaseRoutine, RoutineExecutor
import re

pattern = re.compile(r'(?<!^)(?=[A-Z])')
def camel_to_snake(name):
    return pattern.sub('_', name).lower()

class RoutinesCLIBuilder:
    def __init__(self, registry: Registry[BaseRoutine]):
        self.registry = registry
    
    def build(self, group: "click.group"):
        
        @group.group(name="routines")
        def routine_group(**kwargs):
            pass
        
        @routine_group.group(name="run")
        def routine_run(**kwargs):
            pass
        
        for routine in self.registry.getRegistered():
            name_camel_case = camel_to_snake(routine.name)
            
            def cmd_wrapper(r):
                def cmd(**kwargs):
                    executor = RoutineExecutor(r)
                    self.registry.registerExecutor(executor)
                    executor.run(**kwargs)
                cmd = click.command(name=name_camel_case)(cmd)
                
                for name, param in r.getParameters():
                    # if parameter is boolean, make it a flag
                    if param.type == bool:
                        cmd = click.option(
                            f'--{name}',
                            is_flag=True,
                            default=param.default,
                            envvar=param.environment_variable_name,
                            help=param.description
                        )(cmd)
                    else:
                        cmd = click.option(
                            f'--{name}',
                            default=param.default,
                            envvar=param.environment_variable_name
                        )(cmd)
                return cmd
            
            routine_run.add_command(cmd_wrapper(routine), name_camel_case)