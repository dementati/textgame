import sys

from textgame.command import Command, CommandLine
from textgame.state import State


class QuitCommand(Command):
    def __init__(self, state: State):
        super().__init__(state, "quit")

    def execute(self, _cmd_line: CommandLine) -> None:
        sys.exit(0)
