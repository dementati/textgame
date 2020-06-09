import json
from typing import Dict


class Room:
    def __init__(self, room_id: str, description: str, exits: Dict[str, str]):
        self.id = room_id
        self.description = description
        self.exits = exits

    @classmethod
    def from_json(cls, room_id: str, data: dict) -> "Room":
        return Room(room_id, data["description"], data["exits"])

    @classmethod
    def load_rooms(cls, room_file: str) -> Dict[str, "Room"]:
        with open(room_file) as f:
            room_data = json.load(f)
            return {room_id: Room.from_json(room_id, data) for room_id, data in room_data.items()}
