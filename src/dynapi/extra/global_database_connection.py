#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app
import flask
from database import DatabaseConnection


def priority_before_request(fn):
    app.before_request_funcs.setdefault(None, []).insert(0, fn)
    return fn


@priority_before_request
def create_connection():
    if flask.request.path.startswith("/static"):
        return
    flask.g.db_conn = DatabaseConnection()


@app.teardown_request
def close_connection(_):
    conn = getattr(flask.g, 'db_conn', None)
    if conn is not None:
        conn.close()
