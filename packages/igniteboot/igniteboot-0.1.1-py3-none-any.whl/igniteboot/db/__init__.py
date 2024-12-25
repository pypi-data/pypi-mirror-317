import re
from urllib.parse import urlparse
from .base import BaseDatabase
from .mysql import MySQLDatabase
from .sqlite import SQLiteDatabase
from ..config import settings

def create_database(database_url: str = None) -> BaseDatabase:
    url = database_url or settings.DATABASE_URL
    parsed = urlparse(url)

    if parsed.scheme == "sqlite":
        db_path = parsed.path.lstrip("/")
        if not db_path:
            db_path = ":memory:"
        return SQLiteDatabase(db_path=db_path)

    elif parsed.scheme == "mysql":
        host = parsed.hostname or "localhost"
        port = parsed.port or 3306
        user = parsed.username or "root"
        password = parsed.password or ""
        db_name = parsed.path.lstrip("/")
        return MySQLDatabase(host, user, password, db_name, port=port)

    else:
        raise ValueError(f"Unsupported database scheme: {parsed.scheme}")
