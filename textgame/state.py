from typing import Dict

from textgame.room import Room


class State:
    def __init__(self, config: dict, rooms: Dict[str, Room]):
        self.rooms = rooms
        self.current_room = rooms[config["initial_room"]]

    @classmethod
    def load_state(cls, config: dict) -> "State":
        rooms = Room.load_rooms(config["room_file"])
        return State(config, rooms)
