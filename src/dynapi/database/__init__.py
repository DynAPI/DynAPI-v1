#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import psycopg2 as psql
import psycopg2.extras
from apiconfig import config


CursorType = t.TypeVar("CursorType")


class DatabaseConnection:
    conn: psql.extras.NamedTupleConnection = None

    def __enter__(self):
        if self.conn:
            raise RuntimeError("don't use this a second time")
        self.conn = psql.connect(
            database=config.get("database", "db_database"),
            user=config.get("database", "db_user"),
            password=config.get("database", "db_password"),
            host=config.get("database", "db_host", fallback="localhost"),
            port=config.getint("database", "db_port", fallback=5432),
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def cursor(self, cursor_factory: t.Type[CursorType] = psql.extras.NamedTupleCursor) -> CursorType:
        return self.conn.cursor(cursor_factory=cursor_factory)
