import re

import click

from baseapp.registry import Registry
from baseapp.registry.routines import BaseRoutine, RoutineExecutor
from baseapp.cli.LazyGroup import LazyGroup

pattern = re.compile(r'(?<!^)(?=[A-Z])')
def camel_to_snake(name):
    return pattern.sub('_', name).lower()

class RoutinesCLIBuilder:
    def __init__(self, registry: Registry[BaseRoutine]):
        self.registry = registry
    
    def buildLazy(self, group: "click.group"):
        @group.group(name="routines")
        def routines():
            pass
        
        @routines.group(
            name="run",
            cls=LazyGroup,
            registry=self.registry,
            cliBuilder=self
        )
        def routines_run():
            pass
            
    def buildCommand(self, cmdName, routine: BaseRoutine):
        
        @click.pass_context
        def cmd(ctx, **kwargs):
            more_kwargs = dict()
            for item in ctx.args:
                option, value = item.split('=')
                option = option.strip("-")
                more_kwargs.update([(option, value)])
            kwargs.update(more_kwargs)
            
            executor = RoutineExecutor(routine)
            # process = Process(target=executor.run, kwargs=kwargs)
            self.registry.registerExecutor((executor, None))
            # process.start()
            # process.join()
            executor.run(**kwargs)
        cmd = click.command(name=cmdName,
                            context_settings=dict(
                                ignore_unknown_options=True,
                                allow_extra_args=True))(cmd)
        
        for name, param in routine.getParameters():
            # if parameter is boolean, make it a flag
            if param.name is not None:
                name = param.name
            if param.type == bool:
                cmd = click.option(
                    f'--{name}', f"{name}",
                    is_flag=True,
                    default=param.default,
                    envvar=param.environment_variable_name,
                    help=param.description
                )(cmd)
            else:
                cmd = click.option(
                    f'--{name}', f"{name}",
                    default=param.default,
                    envvar=param.environment_variable_name,
                    type=param.type,
                    help=param.description,
                    required=param.required
                )(cmd)
        return cmd