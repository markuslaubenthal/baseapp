import click
from ..registry import Registry
from ..registry.services import BaseService, ServiceExecutor
import re

pattern = re.compile(r'(?<!^)(?=[A-Z])')
def camel_to_snake(name):
    return pattern.sub('_', name).lower()

class ServicesCLIBuilder:
    def __init__(self, registry: Registry[BaseService]):
        self.registry = registry
    
    def build(self, group: "click.group"):
        
        @group.group(name="services")
        def service_group(**kwargs):
            pass
        
        @service_group.group(name="run")
        def service_run(**kwargs):
            pass
        
        for service in self.registry.getRegistered():
            name_camel_case = camel_to_snake(service.name)
            
            def cmd_wrapper(r):
                def cmd(**kwargs):
                    import pickle
                    executor = ServiceExecutor(r)
                    # pickle.dumps(executor.service)
                    executor.setArguments(**kwargs)
                    self.registry.registerExecutor(executor)
                    executor.start()
                    executor.join()
                cmd = click.command(name=name_camel_case)(cmd)
                
                for name, param in r.getParameters():
                    cmd = click.option(
                        f'--{name}',
                        default=param.default,
                        envvar=param.environment_variable_name
                    )(cmd)
                return cmd
            
            service_run.add_command(cmd_wrapper(service), name_camel_case)