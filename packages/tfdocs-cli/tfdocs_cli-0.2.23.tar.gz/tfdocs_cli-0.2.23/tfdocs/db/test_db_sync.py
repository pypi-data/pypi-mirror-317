import asyncio
import tempfile
import sqlite3
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from tfdocs.db import TEST_DB_URL
from tfdocs.db.test_handler import MockDb
from tfdocs.db.sync import (
    parse_schemas,
    main,
    load_local_schemas,
    fetch_schemas,
    parse_block,
    parse_attribute,
    block_iter,
    db_insert_batch,
)
from tfdocs.models.test_block import MockBlock
import logging


async def fetch_test_schemas() -> asyncio.StreamReader:
    process = await asyncio.subprocess.create_subprocess_exec(
        *["cat", "tests/test_schemas.json"],
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    if process.stdout is None:
        raise OSError("Couldn't fetch the test data to parse")
    return process.stdout


@pytest.mark.asyncio
async def test_fetch_test_schemas():
    mock_stdout = AsyncMock()
    mock_stdout.read = AsyncMock(return_value=b'{"test_schema": "value"}')

    mock_process = AsyncMock()
    mock_process.stdout = mock_stdout

    # Patch create_subprocess_exec to return our mocked process
    with patch("asyncio.subprocess.create_subprocess_exec", return_value=mock_process):
        result = await fetch_test_schemas()
        assert result == mock_stdout

    mock_process = AsyncMock()
    mock_process.stdout = None

    # Patch create_subprocess_exec to return our mocked process
    with patch("asyncio.subprocess.create_subprocess_exec", return_value=mock_process):
        with pytest.raises(OSError, match="Couldn't fetch the test data to parse"):
            await fetch_test_schemas()


@patch("rich.status.Status")
@pytest.mark.asyncio
async def test_db_sync(mock_status):
    with MockDb().cx as cx:
        cursor = cx.cursor()
        await parse_schemas(cursor, await fetch_test_schemas(), mock_status)

        # Verify the block table exists
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='block';"
        )
        assert cursor.fetchone() is not None, "Block table was not created"

        # Verify the attribute table exists
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='attribute';"
        )
        assert cursor.fetchone() is not None, "Attribute table was not created"

        # Verify columns in block table
        cursor.execute("PRAGMA table_info(block);")
        block_columns = [info[1] for info in cursor.fetchall()]
        expected_block_columns = [
            "block_id",
            "block_type",
            "block_name",
            "parent_id",
        ]
        for col in expected_block_columns:
            assert col in block_columns, f"Column '{col}' is missing from block table"

        # Verify columns in attribute table
        cursor.execute("PRAGMA table_info(attribute);")
        attribute_columns = [info[1] for info in cursor.fetchall()]
        expected_attribute_columns = [
            "attribute_id",
            "attribute_type",
            "attribute_name",
            "description",
            "description_type",
            "optional",
            "computed",
            "block_id",
        ]
        for col in expected_attribute_columns:
            assert (
                col in attribute_columns
            ), f"Column '{col}' is missing from attribute table"


def test_main():
    with patch("tfdocs.db.sync.load_local_schemas") as test_schema_loader:
        main()
        test_schema_loader.assert_called_once()


# Mock functions that will be used
@patch("tfdocs.db.sync.Status")
@patch("tfdocs.db.sync.fetch_schemas", autospec=True)
@patch("tfdocs.db.sync.parse_schemas", autospec=True)
@pytest.mark.asyncio
async def test_load_local_schemas_success(
    mock_parse_schemas, mock_fetch_schemas, mock_status
):
    # Mock database connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    # Mock fetch_schemas return value
    mock_stream = MagicMock()
    mock_fetch_schemas.return_value = mock_stream
    mock_status.return_value.__enter__.return_value = MagicMock()

    # Call the function
    await load_local_schemas(mock_cursor)

    # Assert the cursor and connection interactions
    mock_parse_schemas.assert_called_once_with(
        mock_cursor, mock_stream, mock_status.return_value.__enter__()
    )


@patch("tfdocs.db.sync.fetch_schemas", autospec=True)
@pytest.mark.asyncio
async def test_load_local_schemas(mock_fetch_schemas):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    # Mock fetch_schemas to raise an OSError
    mock_fetch_schemas.side_effect = OSError("Network error")

    # Call the function and capture the output
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        await load_local_schemas(mock_cursor)

    # Assert the OSError was caught and SystemExit was raised
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    mock_cursor.close.assert_not_called()  # No closing cursor since OSError occurred


@patch("rich.status.Status")
@patch("tfdocs.db.sync.parse_block")
@patch("tfdocs.db.sync.db_insert_batch")
@pytest.mark.asyncio
async def test_parse_schemas_success(
    mock_db_insert_batch, mock_parse_block, mock_status
):
    mock_cursor = MagicMock()
    mock_stream = MagicMock()

    async def kvitems_gen():
        yield ("provider_name", {"provider": {"block": "block_data"}})

    with patch("ijson.kvitems_async", return_value=kvitems_gen()) as mock_kvitems_async:
        await parse_schemas(mock_cursor, mock_stream, mock_status)

    # Assertions on mocks should verify correct behavior
    mock_kvitems_async.assert_called_once_with(mock_stream, "provider_schemas")


@patch("rich.status.Status")
@pytest.mark.asyncio
async def test_parse_schemas_error(mock_status):

    async def create_mock_streamreader(fake_data: bytes) -> asyncio.StreamReader:
        stream = asyncio.StreamReader()
        # Use feed_data to simulate passing data to the StreamReader
        stream.feed_data(fake_data)
        # feed_eof signals the end of the stream
        stream.feed_eof()
        return stream

    # Mock cursor and stream
    mock_cursor = MagicMock()
    mock_stream = await create_mock_streamreader(b'{"incomplete_json":"cut-off content')

    with pytest.raises(SystemExit):
        await parse_schemas(mock_cursor, mock_stream, mock_status)


@pytest.mark.asyncio
async def test_fetch_schemas():
    # Create a mock process
    mock_process = MagicMock()

    # Create a mock stdout stream (this would be returned by the subprocess)
    mock_stdout = MagicMock()

    # Mock create_subprocess_exec to return a process with mock stdout
    with patch("asyncio.subprocess.create_subprocess_exec", return_value=mock_process):
        # Set the stdout attribute to the mock stdout
        mock_process.stdout = mock_stdout

        # Call the fetch_schemas function
        result = await fetch_schemas()

        # Assert that the function returned the stdout stream
        assert result == mock_stdout

        # Assert that the subprocess was called with the correct arguments
        asyncio.subprocess.create_subprocess_exec.assert_called_once_with(
            *["terraform", "providers", "schema", "-json"],
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )


@pytest.mark.asyncio
async def test_fetch_schemas_no_stdout():
    # Create a mock process
    mock_process = MagicMock()

    # Mock create_subprocess_exec to return a process with None stdout
    with patch("asyncio.subprocess.create_subprocess_exec", return_value=mock_process):
        # Set the stdout attribute to None
        mock_process.stdout = None

        # Expect the function to raise an OSError due to None stdout
        with pytest.raises(OSError, match="Couldn't find any config in this directory"):
            await fetch_schemas()

        # Assert that the subprocess was called with the correct arguments
        asyncio.subprocess.create_subprocess_exec.assert_called_once_with(
            *["terraform", "providers", "schema", "-json"],
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )


def test_parse_none_block():
    assert None == parse_block("test", None, "misc", None)
    test_res = parse_block(
        "test", {"block_types": {"inner_block": {"block": {}}}}, "misc", None
    )
    assert len(test_res.blocks) == 1


def test_block_iter():
    with patch("tfdocs.db.sync.parse_block", return_value=None) as mock_parse_block:
        res = block_iter(
            {"test_resources": {"resource_1": {"block": {}}}},
            "test_resources",
            "misc",
            None,
        )
        with pytest.raises(StopIteration):
            next(res)


def test_parse_attribute():
    assert None == parse_attribute("test", None, None)
    with pytest.raises(ValueError):
        parse_attribute("test", {"type": 123}, None)


# @mock.patch(
#     "tfdocs.models.block.Block.flatten",
#     return_value=([MockBlock(type="misc")],[]),
#     autospec=True,
# )
@patch("rich.status.Status")
@patch(
    "tfdocs.models.block.Block.flatten",
    return_value=([MockBlock(type="misc", name="test_block")], []),
    autospec=True,
)
def test_db_insert_batch_error(mock_flatten, mock_status):
    class TempDb(MockDb):
        _connection = None
        _db_url = tempfile.mktemp()

    mock_block = MockBlock(type="misc")
    with TempDb().cx as cursor:
        with pytest.raises(SystemExit):
            db_insert_batch([mock_block], cursor, mock_status)
