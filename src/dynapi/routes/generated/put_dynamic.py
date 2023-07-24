#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app
import flask
from flask import request, g
from pypika import PostgreSQLQuery as Query, Schema, Table, Criterion
from database import DatabaseConnection, dbutil
import apiconfig
from apiutil import makespec, get_body_config


@app.route("/api/db/<string:schemaname>/<string:tablename>", methods=["PUT"])
def put(schemaname: str, tablename: str):
    apiconfig.flask_method_check()
    body = get_body_config(request)
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
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
        g.SQL = str(query)
        return flask.jsonify([
           {col.name: row[index] for index, col in enumerate(cursor.description)}
           for row in cursor.fetchall()
        ])


def get_openapi_spec(connection: DatabaseConnection, tables_meta):
    spec = {}
    for table in dbutil.list_tables(connection=connection):
        if apiconfig.method_check(method="put", schema=table.schema, table=table.table):
            spec.update(
                makespec(method="put", schemaname=table.schema, tablename=table.table,
                         columns=tables_meta[table.schema][table.table])
            )
    return spec
