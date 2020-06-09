from command import Command


class LookCommand(Command):
    def __init__(self, state):
        super().__init__(state, "look")

    def execute(self, _cmd_input):
        print(self.state.current_room.description)
