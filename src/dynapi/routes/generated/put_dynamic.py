#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app
import flask
from flask import request
from pypika import PostgreSQLQuery as Query, Schema, Table, Criterion, FormatParameter
from database import dbutil
import apiconfig
from apiutil import makespec, get_body_config, responsify


@app.put("/api/<string:schemaname>/<string:tablename>")
def put(schemaname: str, tablename: str):
    apiconfig.flask_method_check()
    body = get_body_config(request)
    with flask.g.db_conn as conn:
        cursor = conn.cursor()
        schema = Schema(schemaname)
        table = Table(tablename)
        query = Query \
            .update(schema.__getattr__(tablename)) \

        for attr in body.obj.keys():
            query = query.set(table.__getattr__(attr), FormatParameter())

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
        cursor.execute(query, body.obj.values())
        conn.commit()
        return responsify(cursor)
        # return responsify([
        #     {col.name: row[index] for index, col in enumerate(cursor.description)}
        #     for row in cursor.fetchall()
        # ])


def get_openapi_spec(tables_meta):
    spec = {}
    connection=flask.g.db_conn
    for table in dbutil.list_tables(connection=connection):
        if apiconfig.method_check(method="put", schema=table.schema, table=table.table):
            spec.update(
                makespec(method="put", schemaname=table.schema, tablename=table.table,
                         columns=tables_meta[table.schema][table.table])
            )
    return spec
