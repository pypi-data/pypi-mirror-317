import sqlite3
from typing import Any, Tuple
from .base import BaseDatabase

class SQLiteDatabase(BaseDatabase):
    def __init__(self, db_path: str):
        self.db_path = r"{}".format(db_path)
        self._conn = None

    def connect(self) -> None:
        if not self._conn:
            self._conn = sqlite3.connect(self.db_path, check_same_thread=False)

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None

    def execute(self, query: str, params: Tuple[Any, ...] = ()):
        self.connect()
        try:
            cursor = self._conn.cursor()
            cursor.execute(query, params)
            self._conn.commit()
            return cursor
        except Exception:
            self._conn.rollback()
            raise

    def fetchall(self, query: str, params: Tuple[Any, ...] = ()) -> list:
        self.connect()
        try:
            cursor = self._conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return rows
        except Exception:
            self._conn.rollback()
            raise
