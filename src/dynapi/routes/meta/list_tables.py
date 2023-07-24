#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import flask
from __main__ import app
from database import DatabaseConnection, dbutil
from apiutil import make_schema, schematypes as s


@app.route("/api/{schemaname}/list-tables", methods=["OPTIONS"])
def list_tables():
    return flask.jsonify(dbutil.list_tables())


def get_openapi_spec(_):
    return {
        '/api/list-tables': {
            'options': make_schema(
                tags=["Meta"],
                summary="Gets Schema and Table-names",
                responses={
                    200: s.Array(
                        s.Object(
                            schema=s.String(),
                            name=s.String(),
                            type=s.String().enum(["table", "view"])
                        )
                    )
                }
            )
        }
    }
