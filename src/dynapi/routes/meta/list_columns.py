#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app
import flask
from database import DatabaseConnection, dbutil
from apiutil.makespec import POSTGRES2OPENAPI
from apiutil import make_schema, schematypes as s


@app.route("/api/meta/<string:schemaname>/<string:tablename>/list-columns")
def columns(schemaname: str, tablename: str):
    with DatabaseConnection() as connection:
        cols = dbutil.list_columns(connection=connection, schema=schemaname, table=tablename)
        return flask.jsonify({
            col.name: POSTGRES2OPENAPI.get(col.data_type)['type']
            for col in cols
        })


def get_openapi_spec(_, __):
    return {
        '/api/meta/{schemaname}/{tablename}/list-columns': {
            'get': make_schema(
                tags=["Meta"],
                summary="Gets all columns of a specific table within a schema",
                path=dict(
                    schema={
                        'description': "Database Schema",
                        'schema': s.String(),
                    },
                    table={
                        'description': "Database Table Name",
                        'schema': s.String(),
                    },
                ),
                responses={
                    200: s.Array(
                        s.Object(
                            column_name=s.String(),
                            data_type=s.String(),
                        )
                    )
                }
            )
        }
    }
