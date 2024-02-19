import click
import re

pattern = re.compile(r'(?<!^)(?=[A-Z])')
def camel_to_snake(name):
    return pattern.sub('_', name).lower()

class LazyGroup(click.Group):
    def __init__(self, registry = None, cliBuilder = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # lazy_subcommands is a map of the form:
        #
        #   {command-name} -> {module-name}.{command-object-name}
        #
        self.registry = registry
        self.cliBuilder = cliBuilder
        self.commandNameMapping = {}

    def resolveCmdName(self, cmdName):
        commands = self.registry.getRegistered()
        for cmd in commands:
            if camel_to_snake(cmd.name) == cmdName:
                return cmd.name
        raise KeyError(f"Command {cmdName} not found")
        
            
    def list_commands(self, ctx):
        base = super().list_commands(ctx)
        
        lazy = [camel_to_snake(cmd.name) for cmd in self.registry.getRegistered()]
        
        return base + lazy

    def get_command(self, ctx, cmdName):
        # cli = self.cliBuilder.build(self, create_new_group=False)
        try:
            originalCmdName = self.resolveCmdName(cmdName)
            command = self.registry.get(originalCmdName)
            cmd = self.cliBuilder.buildCommand(cmdName, command)
        except Exception as e:
            raise click.UsageError(f"Command {cmdName} not found") from e
        
        return cmd