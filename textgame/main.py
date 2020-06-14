from textgame import command
from textgame.state import State


def main() -> None:
    configure_logging()

    state = State.load_state("config.json")
    cmds = command.create_commands(state)

    print(state.current_room.description)
    while True:
        cmd_input: str = input("> ")
        cmd = cmds.select(cmd_input)
        if cmd:
            cmd.execute()
        else:
            print("Unrecognized command")


def configure_logging() -> None:
    import logging
    import sys

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


if __name__ == "__main__":
    main()
