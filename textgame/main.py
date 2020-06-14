import json

from textgame.executor import Executor
from textgame.state import State


def main() -> None:
    config = load_config()
    configure_logging(config)
    state = State.load_state(config, print_output)
    executor = Executor(state)

    while True:
        cmd_input: str = input("> ")
        executor.execute(cmd_input)


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


def print_output(output_str: str) -> None:
    print(output_str)


if __name__ == "__main__":
    main()
