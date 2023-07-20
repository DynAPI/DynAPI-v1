#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app
import http
import base64
import flask
from pypika import PostgreSQLQuery as Query, Schema, Table, Criterion
from database import DatabaseConnection
from .pwutil import compare_password_to_hash


@app.before_request
def verify_authorization():
    if not flask.request.path.startswith("/api"):
        return

    authorization = flask.request.authorization
    if not authorization:
        flask.abort(http.HTTPStatus.UNAUTHORIZED)
    username = authorization.username
    password = authorization.password
    if not username and not password:
        raise flask.abort(http.HTTPStatus.UNAUTHORIZED)

    # schemaname = flask.request.view_args["schemaname"]
    # tablename = flask.request.view_args["tablename"]

    schemaname, tablename = 'dynapi', 'users'
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        table = Table(tablename)
        query = Query \
            .from_(Schema(schemaname).__getattr__(tablename)) \
            .select('*') \
            .where(table.username == username)
        cursor.execute(str(query))
        row = cursor.fetchone()
        if not row:
            raise flask.abort(http.HTTPStatus.UNAUTHORIZED)
        if not compare_password_to_hash(password.encode(), base64.b64decode(row.passwordhash.encode())):
            raise flask.abort(http.HTTPStatus.UNAUTHORIZED)


@app.before_first_request
def create_users_table():
    from pypika import Column

    schemaname, tablename = 'dynapi', 'users'
    with DatabaseConnection() as conn:
        cursor = conn.cursor()

        query = Query \
            .create_table(Schema(schemaname).__getattr__(tablename)) \
            .columns(
                Column("username", "VARCHAR", nullable=False),
                Column("passwordhash", "VARCHAR", nullable=False),
                Column("description", "VARCHAR", nullable=False),
                Column("roles", "VARCHAR[]", nullable=True)) \
            .unique("username") \
            .primary_key("username") \
            .if_not_exists()

        cursor.execute(str(query))
        conn.commit()