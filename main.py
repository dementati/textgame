import command
from state import State

state = State.load_state("config.json")
cmds = command.create_commands(state)

print(state.current_room.description)
while True:
    cmd_input = input("> ")

    cmd_found = False
    for cmd in cmds:
        if cmd.detect(cmd_input):
            cmd.execute(cmd_input)
            cmd_found = True
            break

    if not cmd_found:
        print("Unrecognized command")
