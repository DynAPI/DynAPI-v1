#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import flask
from __main__ import app
from database import DatabaseConnection, dbutil


@app.route("/list-columns/<string:schema>/<string:table>")
def columns(schema: str, table: str):
    with DatabaseConnection() as connection:
        return flask.jsonify(dbutil.list_columns(connection=connection, schema=schema, table=table))


def get_openapi_spec():
    return {
        '/list-columns/{schema}/{table}': {
            'get': {
                'tags': ["Meta"],
                'summary': "Gets all columns of a specific table within a schema",
                'parameters': [
                    {
                        'name': "schema",
                        'in': "path",
                        'description': "Database Schema",
                        'schema': dict(
                            type="string"
                        )
                    },
                    {
                        'name': "table",
                        'in': "path",
                        'description': "Database Table Name",
                        'schema': dict(
                            type="string",
                        ),
                    },
                ],
                'responses': {
                    '200': {
                        'description': "Successful operation",
                        'content': {
                            "application/json": {
                                'schema': {
                                    'type': "array",
                                    'items': {
                                        'type': "object",
                                        'properties': {
                                            'column_name': dict(
                                                type="string"
                                            ),
                                            'is_nullable': dict(
                                                type="string"
                                            ),
                                            'data_type': dict(
                                                type="string"
                                            ),
                                            'is_identity': dict(
                                                type="string"
                                            ),
                                            'is_generated': dict(
                                                type="string"
                                            ),
                                            'is_updatable': dict(
                                                type="string"
                                            ),
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
