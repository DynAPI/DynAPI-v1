#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app
import flask
from flask import request
from pypika import PostgreSQLQuery as Query, Schema, Table
from database import DatabaseConnection, dbutil
from apiconfig import flask_method_check, method_check
from apiutil import makespec, get_body_config


@app.route("/api/db/<string:schemaname>/<string:tablename>", methods=["POST"])
def post(schemaname: str, tablename: str):
    flask_method_check()
    body = get_body_config(request)
    with DatabaseConnection() as conn:
        from psycopg2.extras import NamedTupleCursor
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)
        schema = Schema(schemaname)
        table = Table(tablename)
        query = Query.into(schema.__getattr__(tablename)) \
            .columns(*body.obj.keys()) \
            .insert(*body.obj.values()) \
            .returning("*")

        cursor.execute(str(query))
        conn.commit()
        return flask.jsonify([
            {col.name: row[index] for index, col in enumerate(cursor.description)}
            for row in cursor.fetchall()
        ])


def get_openapi_spec(connection: DatabaseConnection, tables_meta):
    spec = {}
    for table in dbutil.list_tables(connection=connection):
        if method_check(method="post", schema=table.schema, table=table.table):
            spec.update(
                makespec(method="post", schemaname=table.schema, tablename=table.table,
                         columns=tables_meta[table.schema][table.table])
            )
    return spec
