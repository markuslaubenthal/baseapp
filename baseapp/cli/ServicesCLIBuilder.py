import re
from multiprocessing import Process

import click

from ..registry import Registry
from ..registry.services import BaseService, ServiceExecutor
from .LazyGroup import LazyGroup

pattern = re.compile(r'(?<!^)(?=[A-Z])')
def camel_to_snake(name):
    return pattern.sub('_', name).lower()

class ServicesCLIBuilder:
    def __init__(self, registry: Registry[BaseService]):
        self.registry = registry
        
    def buildLazy(self, group: "click.group"):
        @group.group(name="services")
        def services():
            pass
        
        @services.group(
            name="run",
            cls=LazyGroup,
            registry=self.registry,
            cliBuilder=self
        )
        def services_run():
            pass
        
    def buildCommand(self, cmdName, service: BaseService):
        def cmd(**kwargs):
            executor = ServiceExecutor(service)
            executor.setIgnoreInterrupt(True)
            executor.setArguments(**kwargs)
            if service.__start_in_main_thread__:
                self.registry.registerExecutor((executor, None))
                executor.run()
            else:
                executor_process = Process(target=executor.run)
                self.registry.registerExecutor((executor, executor_process))
                executor_process.start()
                # executor_process.join()
                
        cmd = click.command(name=cmdName)(cmd)
        
        for name, param in service.getParameters():
            cmd = click.option(
                f'--{name}',
                default=param.default,
                envvar=param.environment_variable_name
            )(cmd)
        return cmd