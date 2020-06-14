import json

from textgame import command
from textgame.command import CommandException
from textgame.state import State


def main() -> None:
    config = load_config()
    configure_logging(config)
    state = State.load_state(config)
    cmds = command.create_commands(state)

    print(state.current_room.description)
    while True:
        cmd_input: str = input("> ")
        cmd = cmds.select(cmd_input)
        if cmd:
            try:
                cmd.execute()
            except CommandException as e:
                print(e)
        else:
            print("Unrecognized command")


def load_config(config_file: str = "config.json") -> dict:
    with open(config_file) as f:
        return json.load(f)


def configure_logging(config: dict) -> None:
    import logging
    import sys

    if "log_level" in config:
        level = getattr(logging, config["log_level"])
    else:
        level = logging.INFO

    root = logging.getLogger()
    root.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


if __name__ == "__main__":
    main()
