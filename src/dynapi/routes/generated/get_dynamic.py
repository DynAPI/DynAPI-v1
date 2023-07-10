#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import flask
from flask import request
from database import DatabaseConnection
from database import dbutil
from pypika import PostgreSQLQuery as Query, Schema, Table, Criterion
from __main__ import app
from apiconfig import config
from exceptions import DoNotImportException
from apiutil import makespec, makespec_extra
from apiutil import get_body_config


if not config.getboolean("methods", "get", fallback=False):
    raise DoNotImportException()


OPMAP = {
    "==": Criterion.eq,
    "eq": Criterion.eq,
    "!=": Criterion.ne,
    "not": Criterion.ne,
    ">": Criterion.gt,
    ">=": Criterion.gte,
    "<": Criterion.lt,
    "<=": Criterion.lte,
    "glob": Criterion.glob,
    "like": Criterion.like,
}


@app.route("/get/<string:schema>/<string:table>")
def select(schema: str, table: str):
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
                        OPMAP[op.lower()](table.__getattr__(attr), value)
                        for attr, op, value in ands
                    )
                    for ands in body.filters
                )
            )

        if body.limit:
            query = query.limit(body.limit).offset(body.offset)

        cursor.execute(str(query))
        return flask.jsonify([
            {col.name: row[index] for index, col in enumerate(cursor.description)}
            for row in cursor.fetchall()
        ])


def get_openapi_spec(connection: DatabaseConnection, tables_meta):
    spec = {}
    for table in dbutil.list_tables(connection=connection):
        spec.update(
            makespec(method="get", schemaname=table.schema, tablename=table.table,
                     columns=tables_meta[table.schema][table.table])
        )
        spec.update(makespec_extra(schemaname=table.schema, tablename=table.table))
    return spec
