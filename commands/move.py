from command import Command, CommandException


class MoveCommand(Command):
    def __init__(self, state):
        super().__init__(state, "move")

    def detect(self, cmd_input):
        return self.get_target(cmd_input) in self.state.current_room.exits

    def execute(self, cmd_input):
        target = self.get_target(cmd_input)
        room_id = self.state.current_room.exits[target]
        self.state.current_room = self.state.rooms[room_id]
        print(self.state.current_room.description)

    @staticmethod
    def get_target(cmd_input):
        parts = cmd_input.split()

        if parts[0] == "move":
            if len(parts) != 2:
                raise CommandException("Usage: move <target>")

            return parts[1]
        elif len(parts) == 1:
            return parts[0]
