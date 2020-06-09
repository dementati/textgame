from textgame.command import Command
from textgame.state import State


class ExitsCommand(Command):
    def __init__(self, state: State):
        super().__init__(state, "exits")

    def execute(self, _cmd_input: str) -> None:
        print(", ".join(self.state.current_room.exits.keys()))
