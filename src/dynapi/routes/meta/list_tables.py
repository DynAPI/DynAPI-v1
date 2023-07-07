#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import flask
from __main__ import app
from database import DatabaseConnection, dbutil


@app.route("/list-tables")
def list_tables():
    with DatabaseConnection() as conn:
        return flask.jsonify(dbutil.list_tables(connection=conn))


def get_openapi_spec(_, __):
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
    }
