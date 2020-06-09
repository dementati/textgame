from command import Command
from state import State


class LookCommand(Command):
    def __init__(self, state: State):
        super().__init__(state, "look")

    def execute(self, _cmd_input: str) -> None:
        print(self.state.current_room.description)
