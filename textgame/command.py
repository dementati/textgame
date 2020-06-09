from abc import abstractmethod
from typing import List

from textgame.state import State


class CommandException(Exception):
    pass


class Command:
    def __init__(self, state: State, name: str = None):
        self.state = state
        self.name = name

    def detect(self, cmd_input: str) -> bool:
        return cmd_input == self.name

    @abstractmethod
    def execute(self, cmd_input: str) -> None:
        pass


# noinspection PyUnresolvedReferences
from textgame.commands import *


def create_commands(state: State) -> List[Command]:
    return [cls(state) for cls in Command.__subclasses__()]  # type: ignore
