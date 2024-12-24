import pytest
import os
from unittest import mock
from tfdocs.db import TEST_DB_URL
from tfdocs.db.handler import Db
from tfdocs.db.init import create_db


class MockDb(Db):
    _connection = None
    _db_url: str = TEST_DB_URL


class DeletionDb(MockDb):
    _connection = None
    _db_url = ".deletion.db"


def test_singleton():
    db_cx_1 = MockDb()
    db_cx_2 = MockDb()
    assert db_cx_1.cx is db_cx_2.cx


def test_sql_method():
    exp_count = 13
    test_count = MockDb().sql("SELECT COUNT(*) FROM block;").fetchone()[0]
    assert exp_count == test_count


def test_sql_method_with_params():
    exp_count = 0
    test_count = (
        MockDb()
        .sql("SELECT COUNT(*) FROM block WHERE block_id == ?;", ("example",))
        .fetchone()[0]
    )
    assert exp_count == test_count


@pytest.mark.asyncio
async def test_clear_database():
    class ClearDb(MockDb):
        _connection = None
        _db_url = ".clear.db"

    mock_db = ClearDb()
    cursor = mock_db.cx.cursor()

    create_db(cursor)
    cursor.execute(
        "INSERT INTO block (block_id, block_type, block_name) VALUES (?, ?, ?)",
        ("example_id", "example_type", "example_name"),
    )
    print(mock_db._db_url)
    assert 1 == mock_db.sql("SELECT COUNT(*) FROM block;").fetchone()[0]

    mock_db.clear()

    assert 0 == mock_db.sql("SELECT COUNT(*) FROM block;").fetchone()[0]
    mock_db.delete()


@pytest.mark.asyncio
async def test_clear_on_nonexistent_db():
    class ClearDb(MockDb):
        _connection = None
        _db_url = ".clear_2.db"

    mock_db = ClearDb()
    mock_db.cursor = None
    # patch the log function
    with mock.patch("tfdocs.db.handler.log") as mock_logger:
        mock_db.clear()
        mock_logger.error.assert_called_once()
    mock_db.delete()


def test_delete_db():
    # create mock_db for deletion
    mock_db = DeletionDb()
    open(mock_db._db_url, "w").write("Test file")

    # make sure it's been created
    assert os.path.exists(mock_db._db_url)

    mock_db.delete()

    assert not os.path.exists(mock_db._db_url)


def test_delete_db_when_not_exists():
    # create mock_db for deletion
    mock_db = DeletionDb()

    # make sure it's been created
    assert not os.path.exists(mock_db._db_url)

    mock_db.delete()


def test_context_manager():
    test_db = MockDb()
    print("test_db_url:", test_db._db_url)
    cx_1 = None
    cx_2 = None
    with test_db.cx as cx:
        cx_1 = cx
        test = cx.execute("SELECT COUNT(*) FROM block;").fetchone()[0]
        exp = 13
        assert exp == test
    with test_db.cx as cx:
        cx_2 = cx
        test = cx.execute("SELECT COUNT(*) FROM attribute;").fetchone()[0]
        exp = 92
        assert exp == test
    assert cx_1 is cx_2
