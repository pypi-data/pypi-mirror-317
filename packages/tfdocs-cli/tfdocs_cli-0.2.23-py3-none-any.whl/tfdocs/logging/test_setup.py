import pytest
import logging
import os
import time
from unittest import mock
from tfdocs.logging.setup import setup_logs, make_log_file, VerbosityFilter


@pytest.fixture
def mock_time():
    """Fixture to mock the time module."""
    with mock.patch("time.time") as mock_time:
        mock_time.return_value = 1000000  # Fixed timestamp for testing
        yield mock_time


@pytest.fixture
def mock_os():
    """Fixture to mock the os module."""
    with mock.patch("os.makedirs") as mock_makedirs, mock.patch(
        "os.listdir"
    ) as mock_listdir, mock.patch("os.path.isfile") as mock_isfile, mock.patch(
        "os.path.getmtime"
    ) as mock_getmtime, mock.patch(
        "os.remove"
    ) as mock_remove:
        yield {
            "makedirs": mock_makedirs,
            "listdir": mock_listdir,
            "isfile": mock_isfile,
            "getmtime": mock_getmtime,
            "remove": mock_remove,
        }


@pytest.fixture
def mock_tempfile():
    """Fixture to mock the tempfile module."""
    with mock.patch("tempfile.NamedTemporaryFile") as mock_tempfile:
        mock_temp = mock.Mock()
        mock_temp.name = "/tmp/tfdocs/test.log"
        mock_tempfile.return_value = mock_temp
        yield mock_tempfile


@pytest.fixture
def mock_logging_config():
    """Fixture to mock the logging configuration."""
    with mock.patch(
        "tfdocs.logging.setup.logging.config.dictConfig"
    ) as mock_dictConfig, mock.patch(
        "tfdocs.logging.setup.logging.getLogger"
    ) as mock_getLogger:
        mock_logger = mock.Mock()
        mock_getLogger.return_value = mock_logger
        yield {"dictConfig": mock_dictConfig, "logger": mock_logger}


def test_make_log_file(mock_os, mock_tempfile, mock_time):
    """Test the make_log_file function."""
    # Mock listdir to return a file older than 24 hours
    mock_os["listdir"].return_value = ["old_log.log"]
    mock_os["isfile"].return_value = True
    mock_os["getmtime"].return_value = 1000000 - (25 * 60 * 60)  # 25 hours ago

    # Call make_log_file and ensure logs older than 24 hours are removed
    log_file = make_log_file()

    # Assert that the old log was removed and a new one created
    mock_os["remove"].assert_called_once_with("/tmp/tfdocs/old_log.log")
    mock_tempfile.assert_called_once()
    assert log_file == "/tmp/tfdocs/test.log"


def test_setup_logs_no_streaming(mock_logging_config, mock_tempfile):
    """Test the setup_logs function with log streaming disabled."""
    setup_logs(print_log_level=logging.INFO, enable_log_streaming=False)

    # Ensure dictConfig was called
    mock_logging_config["dictConfig"].assert_called_once()

    # Retrieve the actual configuration passed to dictConfig
    config_args = mock_logging_config["dictConfig"].call_args[0][0]

    print(config_args["handlers"])
    # Assert logging configuration was called correctly without streaming
    assert "serve" not in config_args["loggers"]["root"]["handlers"]  # No UDP handler
    assert (
        "file" in config_args["loggers"]["root"]["handlers"]
    )  # File logging is present
    assert (
        "console" in config_args["loggers"]["root"]["handlers"]
    )  # Console logging is present
    mock_logging_config["logger"].info.assert_called_once()
    assert "Logging to" in mock_logging_config["logger"].info.call_args[0][0]


def test_setup_logs_with_streaming(mock_logging_config, mock_tempfile):
    """Test the setup_logs function with log streaming enabled."""
    setup_logs(print_log_level=logging.INFO, enable_log_streaming=True)

    # Ensure dictConfig was called
    mock_logging_config["dictConfig"].assert_called_once()

    # Retrieve the actual configuration passed to dictConfig
    config_args = mock_logging_config["dictConfig"].call_args[0][0]

    # Assert logging configuration was called correctly with streaming
    assert (
        "serve" in config_args["loggers"]["root"]["handlers"]
    )  # UDP handler is present
    assert (
        "file" in config_args["loggers"]["root"]["handlers"]
    )  # File logging is present
    assert (
        "console" in config_args["loggers"]["root"]["handlers"]
    )  # Console logging is present
    mock_logging_config["logger"].info.assert_called_once()
    assert "Logging to" in mock_logging_config["logger"].info.call_args[0][0]


def test_verbosity_filter():
    """Test the VerbosityFilter class."""
    filter_instance = VerbosityFilter(level=logging.INFO)

    # Create a record for different levels
    debug_record = logging.LogRecord(
        name="test",
        level=logging.DEBUG,
        pathname="",
        lineno=0,
        msg="",
        args=(),
        exc_info=None,
    )
    info_record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="",
        args=(),
        exc_info=None,
    )

    # Assert that the filter blocks DEBUG and allows INFO
    assert not filter_instance.filter(debug_record)
    assert filter_instance.filter(info_record)
