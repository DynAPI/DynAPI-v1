#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app
import http
import flask
from flask import request
from pypika import PostgreSQLQuery as Query, Schema, Table, Criterion
from pypika.functions import Count
from database import DatabaseConnection, dbutil
from exceptions import DoNotImportException
from apiconfig import config, flask_method_check, method_check
from apiutil import makespec, get_body_config


if not config.getboolean("methods", "put", fallback=False):
    raise DoNotImportException()


@app.route("/db/<string:schemaname>/<string:tablename>", methods=["PUT"])
def put(schemaname: str, tablename: str):
    flask_method_check()
    body = get_body_config(request)
    with DatabaseConnection() as conn:
        from psycopg2.extras import NamedTupleCursor
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)
        schema = Schema(schemaname)
        table = Table(tablename)
        query = Query \
            .update(schema.__getattr__(tablename)) \

        for attr, value in body.obj.items():
            query = query.set(table.__getattr__(attr), value)

        query = query.where(
                Criterion.any(
                    Criterion.all(
                        dbutil.OPMAP[op.lower()](table.__getattr__(attr), value)
                        for attr, op, value in ands
                    )
                    for ands in body.filters
                )
            )

        query = query.returning("*")
        print(query)
        cursor.execute(str(query))
        conn.commit()
        return flask.jsonify([
           {col.name: row[index] for index, col in enumerate(cursor.description)}
           for row in cursor.fetchall()
        ])


def get_openapi_spec(connection: DatabaseConnection, tables_meta):
    spec = {}
    for table in dbutil.list_tables(connection=connection):
        if method_check(method="put", schema=table.schema, table=table.table):
            spec.update(
                makespec(method="put", schemaname=table.schema, tablename=table.table,
                         columns=tables_meta[table.schema][table.table])
            )
    return spec
