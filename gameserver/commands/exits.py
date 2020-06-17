from gameserver.command import Command, CommandLine, CommandException
from gameserver.state import State


class ExitsCommand(Command):
    def __init__(self, state: State):
        super().__init__(state, "exits")

    def validate(self, cmd_line: CommandLine) -> None:
        if cmd_line.args:
            raise CommandException("Usage: exits")

    def execute(self, _cmd_line: CommandLine) -> None:
        self.state.output("Exits:")
        self.state.output(", ".join(self.state.current_room.exits.keys()))
