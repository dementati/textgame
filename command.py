from abc import abstractmethod


class CommandException(Exception):
    pass


class Command:
    def __init__(self, state, name=None):
        self.state = state
        self.name = name

    def detect(self, cmd_input):
        return cmd_input == self.name

    @abstractmethod
    def execute(self, cmd_input):
        pass


# noinspection PyPep8


def create_commands(state):
    return [cls(state) for cls in Command.__subclasses__()]
