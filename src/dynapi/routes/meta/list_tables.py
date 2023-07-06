#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import flask
from __main__ import app
from database import DatabaseConnection


@app.route("/list-tables")
def list_tables():
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(r"""
        SELECT schemaname, tablename, tableowner
        FROM pg_catalog.pg_tables
        WHERE schemaname != 'information_schema' AND schemaname != 'pg_catalog'
        """)
        return flask.jsonify([
            # {col.name: row[index] for index, col in enumerate(cursor.description)}
            dict(
                schemaname=row.schemaname,
                tablename=row.tablename,
                owner=row.tableowner,
            )
            for row in cursor.fetchall()
        ])


def get_openapi_spec():
    return {
        '/list-tables': {
            'get': {
                'tags': ["Meta"],
                'summary': "Gets Schema and Table-names",
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
                                            'schemaname': {
                                                'type': "string",
                                            },
                                            'tablename': {
                                                'type': "string",
                                            },
                                            'owner': {
                                                'type': "string",
                                            },
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
