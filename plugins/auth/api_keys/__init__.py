#!/usr/bin/python3

"""
https://www.postgresql.org/docs/current/sql-createindex.html
"""
from __main__ import app
import http
import flask
from flask import g
from apiconfig import config
from pypika import PostgreSQLQuery as Query, Schema, Table, Criterion
from database import DatabaseConnection, dbutil
from . import permissions_check


schemaname = config.get('auth', 'schema', fallback="dynapi")
tablename = config.get('auth', 'api_key_table', fallback="api_keys")


@app.before_request
def verify_authorization():
    if not flask.request.path.startswith("/api"):
        return

    api_key = flask.request.headers.get("x-api-key")
    if not api_key:
        raise flask.abort(http.HTTPStatus.UNAUTHORIZED)
    g.user = api_key

    with flask.g.db_conn as conn:
        cursor = conn.cursor()
        table = Table(tablename)
        query = Query \
            .from_(Schema(schemaname).__getattr__(tablename)) \
            .select('*') \
            .where(table.api_key == api_key)
        cursor.execute(str(query))
        row = cursor.fetchone()
        if not row:
            raise flask.abort(http.HTTPStatus.UNAUTHORIZED)
        g.roles = row.roles
    # schemaname = flask.request.view_args["schemaname"]
    # tablename = flask.request.view_args["tablename"]

    # get_roles_allowed(schemaname,tablename)
    #
    # if role in rolesallowed:
    #     raise flask.abort(http.HTTPStatus.UNAUTHORIZED)

#get role from user, then call function that returns list of roles that are allowed to complete this request,
#check if this user has that role, then return true
#rolesallowed=get_roles_allowed(method, schemaname, tablename)


@app.before_first_request
def create_api_keys_table():
    from pypika import Column

    with DatabaseConnection() as conn:
        cursor = conn.cursor()

        query = Query \
            .create_table(Schema(schemaname).__getattr__(tablename)) \
            .columns(
                Column("api_key", "VARCHAR", nullable=False),
                Column("description", "VARCHAR", nullable=False),
                Column("roles", "VARCHAR[]", nullable=True)) \
            .unique("api_key") \
            .primary_key("api_key") \
            .if_not_exists()

        cursor.execute(str(query))
        conn.commit()
