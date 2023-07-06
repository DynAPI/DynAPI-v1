#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import flask
from __main__ import app
from database import DatabaseConnection


@app.route("/list-columns/<string:schema>/<string:tablename>")
def columns(schema: str, tablename: str):
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(r"""
        SELECT *
        FROM information_schema.columns
        WHERE table_schema = %s
        AND table_name   = %s;
        """, [schema, tablename])
        return flask.jsonify([
            dict(
                column_name=row.column_name,
                is_nullable=row.is_nullable,
                data_type=row.data_type,
                is_identity=row.is_identity,
                is_generated=row.is_generated,
                is_updatable=row.is_updatable
            )
            for row in cursor.fetchall()
        ])


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
