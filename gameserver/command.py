import re
from abc import abstractmethod
from copy import copy
from dataclasses import dataclass
from typing import Iterable, Optional, Dict

from gameserver import match
from gameserver.state import State


class CommandException(Exception):
    pass


class CommandLineException(Exception):
    pass


class CommandLine:
    def __init__(self, input_str: str):
        if not input_str.strip():
            raise CommandLineException("Empty input")

        regex = r'(".*")|(\w+)'
        matches = re.findall(regex, input_str)
        tokens = [m1 if m1 else m2 for m1, m2 in matches]
        self.command = tokens[0]
        self.args = tokens[1:]


class Command:
    def __init__(self, state: State, name: str):
        self.state = state
        self.name = name
        self.cmd_line: Optional[CommandLine] = None

    @abstractmethod
    def validate(self, cmd_line: CommandLine) -> None:
        pass

    @abstractmethod
    def execute(self, cmd_line: CommandLine) -> None:
        pass

    def instantiate(self, cmd_line: CommandLine, matcher: str) -> "CommandInstance":
        cmd_line = copy(cmd_line)
        cmd_line.command = matcher
        return CommandInstance(self, cmd_line)

    @property
    def matchers(self) -> Iterable[str]:
        return [self.name]


@dataclass
class CommandInstance:
    cmd: Command
    cmd_line: CommandLine

    def execute(self) -> None:
        self.cmd.validate(self.cmd_line)
        self.cmd.execute(self.cmd_line)


class CommandSet:
    def __init__(self, commands: Iterable[Command]):
        self.commands = commands

    def select(self, input_str: str) -> Optional[CommandInstance]:
        matcher2cmd = self.create_matcher2cmd(self.commands)
        cmd_line = CommandLine(input_str)
        matcher = match.match(cmd_line.command, matcher2cmd.keys())

        if matcher in matcher2cmd:
            return matcher2cmd[matcher].instantiate(cmd_line, matcher)

        return None

    @staticmethod
    def create_matcher2cmd(cmds: Iterable[Command]) -> Dict[str, Command]:
        d = {}
        for cmd in cmds:
            for m in cmd.matchers:
                d[m] = cmd
        return d


# noinspection PyUnresolvedReferences
from gameserver.commands import *


def create_commands(state: State) -> CommandSet:
    return CommandSet([cls(state) for cls in Command.__subclasses__()])  # type: ignore
