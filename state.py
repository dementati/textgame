import json

from room import Room


class State:
    def __init__(self, config, rooms):
        self.rooms = rooms
        self.current_room = rooms[config["initial_room"]]

    @classmethod
    def load_state(cls, config_file):
        with open(config_file) as f:
            config = json.load(f)

        rooms = Room.load_rooms(config["room_file"])

        return State(config, rooms)
