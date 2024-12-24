import pytest
import argparse
import socketserver
from unittest import mock
import logging
import pickle
import socket
from tfdocs.logging.watch_logs import LogServerHandler, main, parse_args


@pytest.fixture
def log_mock():
    """Fixture to mock the logger."""
    with mock.patch("tfdocs.logging.watch_logs.log") as log:
        yield log


def test_parse_args():
    """Test that the watch-logs subcommand is correctly parsed and sets func=main."""

    # Create a mock 'main' function since it will be called when 'watch-logs' is invoked
    with mock.patch("tfdocs.logging.watch_logs.main") as mock_main:
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")

        # Call the function that adds the 'watch-logs' subcommand
        parse_args(subparsers)

        # Simulate passing the 'watch-logs' subcommand on the command line
        args = parser.parse_args(["watch-logs"])

        # Check that the parsed args include the correct func attribute set to 'main'
        assert args.func == mock_main

        # Optionally call the function if you want to simulate full execution:
        args.func(args)
        mock_main.assert_called_once_with(args)


def test_logserver_handler_handle(log_mock):
    """Test the LogServerHandler's handle function."""
    # Create mock data
    # log_record = logging.LogRecord(name="test", level=logging.INFO, pathname="", lineno=0, msg="Test Log", args=(), exc_info=None)
    log_record = {
        "name": "test",
        "level": 20,
        "pathname": "",
        "lineno": 0,
        "msg": "Test Log",
        "args": "()",
        "exc_info": None,
    }
    log_data = pickle.dumps(log_record)
    # Padding the first 4 bytes as per original code (these would normally be metadata or protocol info)
    data = b"0000" + log_data

    # Mock the request (UDP message) and the client address
    mock_request = (data, mock.Mock())
    handler = LogServerHandler(mock_request, ("localhost", 1234), None)

    # Call handle and check if the log record was handled correctly
    # handler.handle()

    # Assert the log record was processed correctly by the logger
    log_mock.handle.assert_called_once()

    # Check the data that was sent back
    mock_request[1].sendto.assert_called_once_with(data.upper(), ("localhost", 1234))


def test_server_starts_and_serves_forever(log_mock):
    """Test the main function starting the server and handling logs."""
    # Mock the UDPServer and the serve_forever method
    with mock.patch.object(
        socketserver.UDPServer, "serve_forever", side_effect=KeyboardInterrupt
    ) as mock_serve_forever:
        with mock.patch(
            "socketserver.UDPServer.__init__", return_value=None
        ):  # To avoid real socket binding
            with mock.patch(
                "socketserver.UDPServer.server_close"
            ):  # To avoid closing a real socket
                # Call the main function
                main()

                # Assert serve_forever was called once
                mock_serve_forever.assert_called_once()

                # Check if the log was correctly handled when server starts and stops
                log_mock.info.assert_called_once_with(
                    f"Listening for logs on port {1234}"
                )
                log_mock.warn.assert_called_once_with("Exited...")
