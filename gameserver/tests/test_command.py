# noinspection Mypy
from pytest import raises

from gameserver.command import CommandLine, CommandLineException


def test_command_line_no_args() -> None:
    # GIVEN
    input_str = 'foo'

    # WHEN
    cmd_line = CommandLine(input_str)

    # THEN
    assert cmd_line.command == "foo"
    assert len(cmd_line.args) == 0


def test_command_line_empty_string() -> None:
    # GIVEN
    input_str = ''

    # EXPECT
    with raises(CommandLineException):
        CommandLine(input_str)


def test_command_line_whitespace_string() -> None:
    # GIVEN
    input_str = ' '

    # EXPECT
    with raises(CommandLineException):
        CommandLine(input_str)


def test_command_line_one_arg() -> None:
    # GIVEN
    input_str = 'foo bar'

    # WHEN
    cmd_line = CommandLine(input_str)

    # THEN
    assert cmd_line.command == "foo"
    assert len(cmd_line.args) == 1
    assert cmd_line.args[0] == "bar"


def test_command_line_two_args() -> None:
    # GIVEN
    input_str = 'foo bar baz'

    # WHEN
    cmd_line = CommandLine(input_str)

    # THEN
    assert cmd_line.command == "foo"
    assert len(cmd_line.args) == 2
    assert cmd_line.args[0] == "bar"
    assert cmd_line.args[1] == "baz"


def test_command_line_one_string_arg() -> None:
    # GIVEN
    input_str = 'foo "bar baz"'

    # WHEN
    cmd_line = CommandLine(input_str)

    # THEN
    assert cmd_line.command == "foo"
    assert len(cmd_line.args) == 1
    assert cmd_line.args[0] == '"bar baz"'
