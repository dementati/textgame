from typing import Iterable, Optional

from gameserver import match
from gameserver.command import Command, CommandException, CommandLine
from gameserver.state import State


class MoveCommand(Command):
    def __init__(self, state: State):
        super().__init__(state, "move")

    def validate(self, cmd_line: CommandLine) -> None:
        if len(cmd_line.args) > 1:
            raise CommandException("Usage: <exit>|move <exit>")

    def execute(self, cmd_line: CommandLine) -> None:
        target = self.get_target(cmd_line)

        if not target:
            raise CommandException("Couldn't find target")

        room_id = self.state.current_room.exits[target]
        self.state.current_room = self.state.rooms[room_id]
        self.state.output(self.state.current_room.description)

    @property
    def matchers(self) -> Iterable[str]:
        return [self.name] + list(self.state.current_room.exits.keys())

    def get_target(self, cmd_line: CommandLine) -> Optional[str]:
        if cmd_line.command == self.name:
            return match.match(cmd_line.args[0], self.state.current_room.exits.keys())
        else:
            return cmd_line.command
