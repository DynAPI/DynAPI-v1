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
from apiutil import makespec, format_name, get_body_config, make_schema, schematypes as s


@app.get("/api/<string:schemaname>/<string:tablename>")
def get(schemaname: str, tablename: str):
    apiconfig.flask_method_check()
    body = get_body_config(request)
    with DatabaseConnection() as conn:
        cursor = conn.cursor()

        schema = Schema(schemaname)
        table = Table(tablename)

        query = Query \
            .from_(schema.__getattr__(tablename)) \
            .select(*body.columns) \
            .where(
                Criterion.any(
                    Criterion.all(
                        dbutil.OPMAP[op.lower()](table.__getattr__(attr), value)
                        for attr, op, value in ands
                    )
                    for ands in body.filters
                )
            )

        if body.limit:
            query = query.limit(body.limit)
        if body.offset:
            query = query.offset(body.offset)

        cursor.execute(str(query))
        g.SQL = str(query)
        return flask.jsonify([
            {col.name: row[index] for index, col in enumerate(cursor.description)}
            for row in cursor.fetchall()
        ])


@app.route("/api/db/<string:schema>/<string:table>/count", methods=["GET"])
def countItems(schema: str, table: str):
    return flask.jsonify(dbutil.get_count(schema=schema, table=table))


def get_openapi_spec(connection: DatabaseConnection, tables_meta):
    spec = {}
    for table in dbutil.list_tables(connection=connection):
        if apiconfig.method_check(method="get", schema=table.schema, table=table.table):
            spec.update(
                makespec(method="get", schemaname=table.schema, tablename=table.table,
                         columns=tables_meta[table.schema][table.table])
            )
            spec.update({
                f'/api/db/{table.schema}/{table.table}/count': {
                    f'get': make_schema(
                        tags=[f"{format_name(table.schema)}/{format_name(table.table)}"],
                        summary=f"Get count for {format_name(table.table)}",
                        # 'description': f"{method} {format_name(tablename)}",
                        responses={
                            200: s.Object(
                                count=s.Integer(),
                            )
                        }
                    )
                }
            })
    return spec
