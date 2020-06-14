from textgame.command import Command, CommandLine, CommandException
from textgame.state import State


class LookCommand(Command):
    def __init__(self, state: State):
        super().__init__(state, "look")

    def validate(self, cmd_line: CommandLine) -> None:
        if cmd_line.args:
            raise CommandException("Usage: look")

    def execute(self, _cmd_line: CommandLine) -> None:
        self.state.output(self.state.current_room.description)
