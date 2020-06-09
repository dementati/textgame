from command import Command


class ExitsCommand(Command):
    def __init__(self, state):
        super().__init__(state, "exits")

    def execute(self, _cmd_input):
        print(", ".join(self.state.current_room.exits.keys()))
