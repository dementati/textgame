from textgame.command import Command, CommandLine
from textgame.state import State


class LookCommand(Command):
    def __init__(self, state: State):
        super().__init__(state, "look")

    def execute(self, _cmd_line: CommandLine) -> None:
        print(self.state.current_room.description)
