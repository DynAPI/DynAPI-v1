#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import flask
from __main__ import app
from database import DatabaseConnection, dbutil
from apiutil import make_schema, schematypes as s


@app.route("/list-tables")
def list_tables():
    with DatabaseConnection() as conn:
        return flask.jsonify(dbutil.list_tables(connection=conn))


def get_openapi_spec(_, __):
    return {
        '/list-tables': {
            'get': make_schema(
                tags=["Meta"],
                summary="Gets Schema and Table-names",
                responses={
                    200: s.Array(
                        s.Object(
                            schema=s.String(),
                            name=s.String(),
                        )
                    )
                }
            )
        }
    }
