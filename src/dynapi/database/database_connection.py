#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import flask
from pypika.queries import QueryBuilder
import psycopg2 as psql
import psycopg2.extras
from apiconfig import config


class CustomCursor(psql.extras.NamedTupleCursor):
    def execute(self, query, vars=None):
        if isinstance(query, QueryBuilder):
            query = query.get_sql()
        if flask.has_app_context():
            flask.g.SQL = query
        return super().execute(query, vars)

    def executemany(self, query, vars):
        if isinstance(query, QueryBuilder):
            query = query.get_sql()
        if flask.has_app_context():
            flask.g.SQL = query
        return super().executemany(query, vars)


class DatabaseConnection:
    conn: psql.extras.NamedTupleConnection = None

    def __init__(self):
        self.conn = psql.connect(
            database=config.get("database", "database"),
            user=config.get("database", "user"),
            password=config.get("database", "password"),
            host=config.get("database", "host", fallback="localhost"),
            port=config.getint("database", "port", fallback=5432),
            connect_timeout=config.getint("database", "connect_timeout", fallback=5),
            cursor_factory=CustomCursor,
        )

    def __del__(self):
        if getattr(self, 'conn') and not self.conn.closed:
            self.conn.close()

    close = __del__

    def __enter__(self):
        self.conn.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.__exit__(exc_type, exc_val, exc_tb)

    def cursor(self) -> CustomCursor:
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()
