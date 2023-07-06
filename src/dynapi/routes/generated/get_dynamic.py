#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import flask
from flask import request
from database import DatabaseConnection
from database import dbutil
from pypika import PostgreSQLQuery as Query, Schema, Table
from __main__ import app
from apiconfig import config
from exceptions import DoNotImportException
from util import makespec


if not config.get("methods", "get"):
    raise DoNotImportException()


@app.route("/get/<string:schema>/<string:table>")
def select(schema: str, table: str):
    with DatabaseConnection() as conn:
        from psycopg2.extras import NamedTupleCursor
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)

        schema = Schema(schema)

        query = Query \
            .from_(schema.__getattr__(table)) \
            .select("*")

        table = Table(table)

        for column, value in request.args.items():
            query = query.where(table.__getattr__(column) == value)

        cursor.execute(str(query))
        return flask.jsonify([
            {col.name: row[index] for index, col in enumerate(cursor.description)}
            for row in cursor.fetchall()
        ])


def get_openapi_spec():
    spec = {}
    with DatabaseConnection() as conn:
        for table in dbutil.list_tables(connection=conn):
            spec.update(makespec(connection=conn, method="get", schemaname=table.schema, tablename=table.table))
    return spec
