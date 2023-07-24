#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app
import flask
from database import DatabaseConnection, dbutil
from apiutil import make_schema, schematypes as s


@app.route("/api/<string:schema>/<string:table>/list-constraints", methods=["OPTIONS"])
def getConstraints(schema: str, table: str):
    return flask.jsonify(
        dbutil.get_constraints(schema=schema, table=table)
    )


def get_openapi_spec(_, __):
    return {
        '/api/{schemaname}/{tablename}/constraints': {
            'options': make_schema(
                tags=["Meta"],
                summary="Get the constrains of a table",
                responses={
                    200: s.Array(
                        s.Object(
                            constraint_name=s.String(),
                            constraint_type=s.String(),
                            referenced_table_name=s.String(),
                            referenced_column_name=s.String(),
                            data_type=s.String(),
                            is_updatable=s.String(),
                        )
                    )
                }
            )
        }
    }
