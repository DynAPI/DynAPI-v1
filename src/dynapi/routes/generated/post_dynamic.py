#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app
import flask
from flask import request, g
from pypika import PostgreSQLQuery as Query, Schema, Table
from database import DatabaseConnection, dbutil
import apiconfig
from apiutil import makespec, get_body_config, responsify


@app.post("/api/<string:schemaname>/<string:tablename>")
def post(schemaname: str, tablename: str):
    apiconfig.flask_method_check()
    body = get_body_config(request)
    with flask.g.db_conn as conn:
        cursor = conn.cursor()
        schema = Schema(schemaname)
        table = Table(tablename)
        query = Query.into(schema.__getattr__(tablename)) \
            .columns(*body.obj.keys()) \
            .insert(*body.obj.values()) \
            .returning("*")

        cursor.execute(query)
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
        if apiconfig.method_check(method="post", schema=table.schema, table=table.table):
            spec.update(
                makespec(method="post", schemaname=table.schema, tablename=table.table,
                         columns=tables_meta[table.schema][table.table])
            )
    return spec
