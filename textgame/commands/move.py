from typing import Iterable

from textgame.command import Command, CommandException, CommandLine
from textgame.state import State


class MoveCommand(Command):
    def __init__(self, state: State):
        super().__init__(state, "move")

    def execute(self, cmd_line: CommandLine) -> None:
        if cmd_line.command == self.name:
            target = cmd_line.args[0]
        else:
            target = cmd_line.command

        if not target:
            raise CommandException("Couldn't find target")

        room_id = self.state.current_room.exits[target]
        self.state.current_room = self.state.rooms[room_id]
        print(self.state.current_room.description)

    @property
    def matchers(self) -> Iterable[str]:
        return [self.name] + list(self.state.current_room.exits.keys())
