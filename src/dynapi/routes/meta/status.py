#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app, __version__
import typing as t
from dataclasses import dataclass
import flask
import psycopg2 as psql
import psycopg2.errorcodes
from database import DatabaseConnection


@dataclass(frozen=True)
class Status:
    online: bool
    version: str
    database: 'Database'


@dataclass(frozen=True)
class Database:
    available: bool
    problem: t.Optional[str]
    problem_detail: t.Optional[str]


@app.route("/status")
def status():
    try:
        with DatabaseConnection():
            pass
    except psql.Error as exc:
        database = Database(
            available=False,
            problem=type(exc).__name__,
            problem_detail=exc.pgcode and psql.errorcodes.lookup(exc.pgcode),
        )
    else:
        database = Database(
            available=True,
            problem=None,
            problem_detail=None
        )

    return flask.jsonify(
        Status(
            online=True,
            version=__version__,
            database=database
        )
    )


def get_openapi_spec(_, __):
    return {
        '/status': {
            'get': {
                'tags': ["Meta"],
                'summary': "Check status of API and Database",
                'responses': {
                    '200': {
                        'description': "Successful operation",
                        'content': {
                            "application/json": {
                                'schema': {
                                    'type': "object",
                                    'properties': {
                                        'online': {
                                            'type': "boolean",
                                        },
                                        'version': {
                                            'type': "string",
                                        },
                                        'database': {
                                            'type': "object",
                                            'properties': {
                                                'online': {
                                                    'type': "boolean",
                                                },
                                                'problem': {
                                                    'type': "string",
                                                    'nullable': True,
                                                },
                                                'problem_detail': {
                                                    'type': "string",
                                                    'nullable': True,
                                                },
                                            }
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
