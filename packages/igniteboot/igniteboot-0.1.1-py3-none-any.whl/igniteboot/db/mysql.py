
import pymysql
from typing import Any, Tuple
from .base import BaseDatabase

class MySQLPool:
    def __init__(self, maxsize=5, **kwargs):
        self._maxsize = maxsize
        self._connections = []
        self._kwargs = kwargs

    def get_connection(self):
        if self._connections:
            return self._connections.pop()
        else:
            return pymysql.connect(**self._kwargs)

    def release_connection(self, conn):
        if len(self._connections) < self._maxsize:
            self._connections.append(conn)
        else:
            conn.close()

class MySQLDatabase(BaseDatabase):
    def __init__(self, host, user, password, db_name, port=3306, max_pool_size=5):
        self.pool = MySQLPool(
            maxsize=max_pool_size,
            host=host,
            user=user,
            password=password,
            db=db_name,
            port=port,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self._conn = None

    def connect(self) -> None:
        if not self._conn:
            self._conn = self.pool.get_connection()

    def close(self) -> None:
        if self._conn:
            self.pool.release_connection(self._conn)
            self._conn = None

    def execute(self, query: str, params: Tuple[Any, ...] = ()):
        self.connect()
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(query, params)
            self._conn.commit()
            return cursor
        except Exception:
            self._conn.rollback()
            raise

    def fetchall(self, query: str, params: Tuple[Any, ...] = ()) -> list:
        self.connect()
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall()
            return rows
        except Exception:
            self._conn.rollback()
            raise
