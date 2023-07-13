#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import sys
import typing as t
import psycopg2 as psql
import psycopg2.extras
from apiconfig import config
from util import TCodes


CursorType = t.TypeVar("CursorType")


class DatabaseConnection:
    conn: psql.extras.NamedTupleConnection = None

    def __enter__(self):
        if self.conn:
            raise RuntimeError("don't use this a second time")
        self.conn = psql.connect(
            database=config.get("database", "database"),
            user=config.get("database", "user"),
            password=config.get("database", "password"),
            host=config.get("database", "host", fallback="localhost"),
            port=config.getint("database", "port", fallback=5432),
            connect_timeout=config.getint("database", "connect_timeout", fallback=5),
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def cursor(self, cursor_factory: t.Type[CursorType] = psql.extras.NamedTupleCursor) -> t.Union[psql.extras.NamedTupleCursor, CursorType]:
        return self.conn.cursor(cursor_factory=cursor_factory)

    def commit(self):
        self.conn.commit()


def test_database_connection():
    try:
        with DatabaseConnection():
            pass
    except Exception as exc:
        print(f"{TCodes.FG_RED}Failed to connect to Database{TCodes.RESTORE_FG}")
        print(f"{type(exc).__name__}: {exc}")
        sys.exit(1)
