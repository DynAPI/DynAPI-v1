#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app
import flask
from flask import request, g
from pypika import PostgreSQLQuery as Query, Schema, Table, Criterion
from database import dbutil
import apiconfig
from apiutil import get_body_config, makespec, responsify


@app.delete("/api/<string:schemaname>/<string:tablename>")
def delete(schemaname: str, tablename: str):
    apiconfig.flask_method_check()
    body = get_body_config(request)
    with flask.g.db_conn as conn:
        cursor = conn.cursor()
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
        cursor.execute(query)

        conn.commit()
        return responsify(cursor)
        # return responsify([
        #     {col.name: row[index] for index, col in enumerate(cursor.description)}
        #     for row in cursor.fetchall()
        # ])


def get_openapi_spec(tables_meta):
    connection = flask.g.db_conn
    spec = {}
    for table in dbutil.list_tables(connection=connection):
        if apiconfig.method_check(method="delete", schema=table.schema, table=table.table):
            spec.update(
                makespec(method="delete", schemaname=table.schema, tablename=table.table,
                         columns=tables_meta[table.schema][table.table])
            )
    return spec
