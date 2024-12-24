import os
import sqlite3
import logging
import threading
from tfdocs.db import DB_URL
from typing import Tuple

log = logging.getLogger()

lock = threading.Lock()


class Db:
    _connection: sqlite3.Connection | None = None
    _db_url: str = DB_URL

    def __init__(self):
        self.cx = self.get_connection()

    @classmethod
    def get_connection(cls) -> sqlite3.Connection:
        if cls._connection is None:
            cls._connection = sqlite3.connect(cls._db_url, check_same_thread=False)
            log.debug("initialising new connection to " + cls._db_url)
        else:
            log.debug("Reusing connection to " + cls._db_url)
        return cls._connection

    @classmethod
    def reset_connection(cls) -> None:
        log.debug(f"Resetting DB connection to {cls._db_url}")
        cls._connection = None

    def sql(self, query: str, params: Tuple | None = None):
        log.debug(f"self._db_url is {self._db_url}")
        cursor = self.cx.cursor()
        try:
            lock.acquire(True)
            if params is None:
                log.debug(f"executing query {query}")
                res = cursor.execute(query)
            else:
                log.debug(f"executing query: {query}\nwith_params: {params}")
                res = cursor.execute(query, params)
        finally:
            lock.release()
        return res

    def clear(self) -> "Db":
        cursor = self.cx.cursor()
        try:
            lock.acquire(True)
            cursor.executescript(
                """
                PRAGMA foreign_keys = OFF;
                BEGIN TRANSACTION;
                DELETE FROM block;
                DELETE FROM attribute;
                COMMIT;
                PRAGMA foreign_keys = ON;
            """
            )
            log.debug(f"Emptied the database {self._db_url}")
        except Exception as e:
            log.error(f"Encountered an issue while clearing the table")
        finally:
            lock.release()
        return self

    @classmethod
    def delete(cls):
        file_path = cls._db_url
        if os.path.exists(file_path):
            os.remove(file_path)
            log.info(f"{file_path} deleted successfully.")
            # da
        else:
            log.info(f"DB '{file_path}' doesn't exist")
