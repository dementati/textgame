import sys

from textgame.command import Command
from textgame.state import State


class QuitCommand(Command):
    def __init__(self, state: State):
        super().__init__(state, "quit")

    def execute(self, _cmd_input: str) -> None:
        sys.exit(0)
