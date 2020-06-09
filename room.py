import json


class Room:
    def __init__(self, room_id, description, exits):
        self.id = room_id
        self.description = description
        self.exits = exits

    @classmethod
    def from_json(cls, room_id, data):
        return Room(room_id, data["description"], data["exits"])

    @classmethod
    def load_rooms(cls, room_file):
        with open(room_file) as f:
            room_data = json.load(f)
            return {room_id: Room.from_json(room_id, data) for room_id, data in room_data.items()}
