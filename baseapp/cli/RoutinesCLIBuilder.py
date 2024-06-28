import click
from ..registry import Registry
from ..registry.routines import BaseRoutine, RoutineExecutor
import re
from .LazyGroup import LazyGroup
from multiprocessing import Process


pattern = re.compile(r'(?<!^)(?=[A-Z])')
def camel_to_snake(name):
    return pattern.sub('_', name).lower()

class RoutinesCLIBuilder:
    def __init__(self, registry: Registry[BaseRoutine]):
        self.registry = registry
    
    # def build(self, group: "click.group"):
        
    #     @group.group(name="routines")
    #     def routine_group(**kwargs):
    #         pass
        
    #     @routine_group.group(name="run")
    #     def routine_run(**kwargs):
    #         pass
        
    #     for routine in self.registry.getRegistered():
    #         name_camel_case = camel_to_snake(routine.name)
            
    #         def cmd_wrapper(r):
    #             def cmd(**kwargs):
    #                 executor = RoutineExecutor(r)
    #                 self.registry.registerExecutor(executor)
    #                 import os
    #                 print("CMDWRAPPER", os.getpid())
    #                 executor.start(**kwargs)
    #             cmd = click.command(name=name_camel_case)(cmd)
                
    #             for name, param in r.getParameters():
    #                 # if parameter is boolean, make it a flag
    #                 if param.type == bool:
    #                     cmd = click.option(
    #                         f'--{name}',
    #                         is_flag=True,
    #                         default=param.default,
    #                         envvar=param.environment_variable_name,
    #                         help=param.description
    #                     )(cmd)
    #                 else:
    #                     cmd = click.option(
    #                         f'--{name}',
    #                         default=param.default,
    #                         envvar=param.environment_variable_name,
    #                         type=param.type,
    #                         help=param.description,
    #                         required=param.required
    #                     )(cmd)
    #             return cmd
            
    #         routine_run.add_command(cmd_wrapper(routine), name_camel_case)
    
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