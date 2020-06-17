from typing import Dict, Callable

from gameserver import command
from gameserver.room import Room

OutputCallback = Callable[[str], None]


class State:
    def __init__(
            self,
            config: dict,
            rooms: Dict[str, Room],
            output: OutputCallback,
    ):
        self.rooms = rooms
        self.current_room = rooms[config["initial_room"]]
        self.commands = command.create_commands(self)
        self.output = output

    @classmethod
    def load_state(cls, config: dict, output: OutputCallback) -> "State":
        rooms = Room.load_rooms(config["room_file"])
        return State(config, rooms, output)
