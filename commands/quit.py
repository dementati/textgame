import sys

from command import Command


class QuitCommand(Command):
    def __init__(self, state):
        super().__init__(state, "quit")

    def execute(self, _cmd_input):
        sys.exit(0)
