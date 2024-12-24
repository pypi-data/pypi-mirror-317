import pytest
import argparse
from unittest import mock
from tfdocs.cli import parse_args
from tfdocs.logging.watch_logs import main as watch_logs

# Mock the watch_logs module, which should define the parse_args function.
# Replace `your_module` with the actual module name where parse_args is located.


@pytest.fixture
def mock_watch_logs():
    with mock.patch("tfdocs.logging.watch_logs.parse_args") as mock_parser:
        yield mock_parser


def test_watch_logs_subcommand():
    """Test the 'watch-logs' subcommand."""
    # Simulate command-line input with the "watch-logs" subcommand
    with mock.patch("sys.argv", ["program_name", "watch-logs"]):
        parser, args = parse_args()
        # Check that the subcommand parser for "watch-logs" was invoked
        assert args["func"] == watch_logs


def test_verbosity_flags():
    """Test that verbosity flags are correctly parsed and validated."""
    with mock.patch("argparse._sys.argv", ["program_name", "-vv"]):
        parser, args = parse_args()
        # Check that verbosity is correctly converted (30 - 10 * 2 == 10 for -vv)
        assert args["verbose"] == 10

    with mock.patch("argparse._sys.argv", ["program_name", "-v"]):
        parser, args = parse_args()
        assert args["verbose"] == 20


def test_invalid_verbosity_flag():
    """Test that invalid verbosity levels raise an error."""
    with mock.patch("argparse._sys.argv", ["program_name", "-vvv"]):
        with pytest.raises(argparse.ArgumentError):
            parse_args()


def test_invalid_command():
    """Test that an invalid subcommand raises an error."""
    with mock.patch("argparse._sys.argv", ["program_name", "invalid-command"]):
        with pytest.raises(SystemExit):
            parse_args()
