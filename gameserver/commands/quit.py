import sys

from gameserver.command import Command, CommandLine, CommandException
from gameserver.state import State


class QuitCommand(Command):
    def __init__(self, state: State):
        super().__init__(state, "quit")

    def validate(self, cmd_line: CommandLine) -> None:
        if cmd_line.args:
            raise CommandException("Usage: quit")

    def execute(self, _cmd_line: CommandLine) -> None:
        self.state.output("Quitting...")
        sys.exit(0)
