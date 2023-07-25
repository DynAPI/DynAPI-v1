#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import time

from __main__ import app
import flask
import psycopg2 as psql
import werkzeug.exceptions
from database import DatabaseConnection


class ConnectionNotAvailable(werkzeug.exceptions.ServiceUnavailable):
    description = "Connection to the database can't be established"


def priority_before_request(fn):
    app.before_request_funcs.setdefault(None, []).insert(0, fn)
    return fn


@priority_before_request
def create_connection():
    flask.g.start_time = time.time()
    if flask.request.path.startswith("/static"):
        return
    try:
        flask.g.db_conn = DatabaseConnection()
    except psql.OperationalError:
        raise ConnectionNotAvailable()


@app.after_request
def add_timing_header(response: flask.Response):
    diff = time.time() - flask.g.start_time
    response.headers.set("x-execution-time", f"{int(diff*1000)}ms")
    return response


@app.teardown_request
def close_connection(_):
    conn = getattr(flask.g, 'db_conn', None)
    if conn is not None:
        conn.close()
