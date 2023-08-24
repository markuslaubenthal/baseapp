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
        for routine in self.registry.getRegistered():
            name_camel_case = camel_to_snake(routine.name)
            
            
            
            def cmd_wrapper(r):
                def cmd(**kwargs):
                    executor = RoutineExecutor(r)
                    executor.run(**kwargs)
                cmd = click.command(name=name_camel_case)(cmd)
                
                for name, param in r.getParameters():
                    cmd = click.option(
                        f'--{name}',
                        default=param.default,
                        envvar=param.environment_variable_name
                    )(cmd)
                return cmd
            
            # executor = RoutineExecutor(routine)
            # new_cmd = click.argument('testarg')(executor.run)
            # new_cmd = click.command(name=name_camel_case)(new_cmd)
            
            group.add_command(cmd_wrapper(routine), name_camel_case)
            # group.add_command(click.command(name=name_camel_case)(executor.run), name_camel_case)
        
        return group