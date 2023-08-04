#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app
import time
from queue import Queue as NewQueue
import atexit
import threading
import typing as t
from datetime import datetime
import flask
from flask import g
from pypika import PostgreSQLQuery as Query, Schema
from apiconfig import config
from database import DatabaseConnection


schemaname = config.get('logging', 'schema') if config.has_option('logging', 'schema') else 'dynapi'
tablename = config.get('logging', 'logging_table') if config.has_option('logging', 'logging_table') else 'audit_log'

queue = NewQueue()


@app.after_request
def logging(response: flask.Response) -> flask.Response:
    if "/api/" in flask.request.path:
        queue.put(dict(
            timestamp=datetime.now(),
            client=flask.request.remote_addr,
            response_code=response.status_code,
            path=flask.request.path,
            method=flask.request.method,
            exception_name=getattr(g, "exception_name", None),
            SQL=getattr(g, "SQL", None),
            user=getattr(g, "user", None),
        ))
    return response


@app.before_first_request
def create_tables():
    from pypika import Column
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        query = Query \
            .create_table(Schema(schemaname).__getattr__(tablename)) \
            .columns(
                Column("id", "SERIAL", nullable=False),
                Column("client", "VARCHAR", nullable=False),
                Column("user", "VARCHAR", nullable=True),
                Column("method", "VARCHAR", nullable=False),
                Column("path", "VARCHAR", nullable=False),
                Column("SQL", "VARCHAR", nullable=True),
                Column("response_code", "SMALLINT", nullable=False),
                Column("exception_name", "VARCHAR", nullable=True),
                Column("timestamp", "TIMESTAMP", nullable=False))\
            .unique("id") \
            .primary_key("id") \
            .if_not_exists()
        cursor.execute(str(query))
        conn.commit()


def log_queue():
    if queue.empty():
        return
    print(f"insert {queue.qsize()} logs into database")
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        schema = Schema(schemaname)
        query = Query.into(schema.__getattr__(tablename)) \
            .columns("client", "user", "method", "path", "SQL", "exception_name", "response_code", "timestamp")

        while not queue.empty():
            record = queue.get()
            query = query.insert(record["client"], record["user"], record["method"], record["path"],
                                 record["SQL"], record["exception_name"], record["response_code"], record["timestamp"])
            queue.task_done()

        cursor.execute(str(query))
        conn.commit()


def logger_worker():
    while app.alive:  # noqa
        try:
            log_queue()
        except Exception as exc:
            print(f"Failed to write log to queue: {type(exc).__name__}: {exc}")
        for _ in range(5):
            if not app.alive:  # noqa
                break
            time.sleep(1)


atexit.register(log_queue)
worker_thread = threading.Thread(target=logger_worker, name="logging-worker", daemon=True)
worker_thread.start()
