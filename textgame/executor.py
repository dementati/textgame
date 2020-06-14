from textgame.command import CommandException
from textgame.state import State


class Executor:
    def __init__(self, state: State):
        self.state = state

    def execute(self, input_str: str) -> None:
        cmd = self.state.commands.select(input_str)
        if cmd:
            try:
                cmd.execute()
            except CommandException as e:
                self.state.output(str(e))
        else:
            self.state.output("Unrecognized command")
