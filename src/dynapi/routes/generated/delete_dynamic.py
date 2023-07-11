#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app
import flask
from flask import request
from database import DatabaseConnection
from database import dbutil
from pypika import PostgreSQLQuery as Query, Schema, Table, Criterion
from apiutil import makespec
from apiconfig import config
from exceptions import DoNotImportException
from apiutil import get_body_config


if not config.getboolean("methods", "delete", fallback=False):
    raise DoNotImportException()


@app.route("/db/<string:schemaname>/<string:tablename>", methods=["DELETE"])
def delete(schemaname: str, tablename: str):
    body = get_body_config(request)
    with DatabaseConnection() as conn:
        from psycopg2.extras import NamedTupleCursor
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)
        schema = Schema(schemaname)
        table = Table(tablename)
        query = Query \
            .from_(schema.__getattr__(tablename)) \
            .delete() \
            .where(
                Criterion.any(
                    Criterion.all(
                        dbutil.OPMAP[op.lower()](table.__getattr__(attr), value)
                        for attr, op, value in ands
                    )
                    for ands in body.filters
                )
            ) \
            .returning("*")

        # if body.limit:
        #     query = query.limit(body.limit).offset(body.offset)

        cursor.execute(str(query))
        # print(f"{cursor.rowcount} rows affected")
        conn.commit()
        return flask.jsonify([
            {col.name: row[index] for index, col in enumerate(cursor.description)}
            for row in cursor.fetchall()
        ])


def get_openapi_spec(connection: DatabaseConnection, tables_meta):
    spec = {}
    for table in dbutil.list_tables(connection=connection):
        spec.update(
            makespec(method="delete", schemaname=table.schema, tablename=table.table,
                     columns=tables_meta[table.schema][table.table])
        )
    return spec
