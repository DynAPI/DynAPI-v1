#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app, __version__
import typing as t
import flask
import psycopg2 as psql
from database import DatabaseConnection
from apiutil import make_schema, schematypes as s
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class Database:
    available: bool
    problem: t.Optional[str]
    problem_detail: t.Optional[str]


@dataclass(frozen=True)
class Status:
    online: bool
    version: str
    database: Database


@app.get("/api/status")
def status():
    try:
        with DatabaseConnection():
            pass
    except psql.Error as exc:
        database = Database(
            available=False,
            problem=type(exc).__name__,
            problem_detail=str(exc),
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
        '/api/status': {
            'get': make_schema(
                tags=["Meta"],
                summary="Check status of API and Database",
                responses={
                    200: s.Object(
                        online=s.Boolean(),
                        version=s.String(),
                        database=s.Object(
                            available=s.Boolean(),
                            problem=s.String().nullable(),
                            problem_detail=s.String().nullable(),
                        )
                    )
                }
            )
        }
    }
