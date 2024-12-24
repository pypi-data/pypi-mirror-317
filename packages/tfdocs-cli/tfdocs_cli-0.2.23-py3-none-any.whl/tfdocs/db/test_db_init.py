import os
import time
import sqlite3
import asyncio
import pytest
import time
from unittest import mock

from tfdocs.db import TEST_DB_URL
from tfdocs.db.init import create_db, main
from tfdocs.db.test_handler import MockDb


class WrappedDb(MockDb):
    _connection = None
    _db_url = ".wrapped.db"


@mock.patch("tfdocs.db.init.load_local_schemas")
@mock.patch("tfdocs.db.init.Db")
@mock.patch("tfdocs.db.init.create_db")
@mock.patch("tfdocs.db.init.check_db")
def test_main(mock_check_db, mock_create_db, mock_db, mock_load_schemas):
    mock_db = WrappedDb()
    main()
    mock_check_db.assert_called_once()
    mock_create_db.assert_called_once()
    mock_load_schemas.assert_called_once()
    mock_db.delete()


def test_db_creation():
    test_db = MockDb()
    cursor = test_db.cx.cursor()
    create_db(cursor)
    res = cursor.execute(
        "SELECT * FROM sqlite_master WHERE type='table' AND name IN ('block', 'attribute');"
    ).fetchall()
    cursor.close()
    assert len(res) == 2
