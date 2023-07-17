#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import psycopg2 as psql
import psycopg2.extras
from apiconfig import config


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
            connection_factory=psql.extras.NamedTupleConnection,
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def cursor(self) -> psql.extras.NamedTupleCursor:
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()
