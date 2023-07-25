#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import re
from database import POSTGRES2OPENAPI
from .schema import make_schema
from . import schematypes as s


METHOD2POP = {
    "get": ["obj"],
    "post": ["columns", "filters", "limit", "offset", "resolve_depth"],
    "delete": ["columns", "obj", "resolve_depth"],
    "put": ["resolve_depth"],
}


def makespec(method: str, schemaname: str, tablename: str, columns):
    return {
        f'/api/db/{schemaname}/{tablename}': {
            f'{method}': make_schema(
                tags=[f"{format_name(schemaname)}/{format_name(tablename)}"],
                summary=format_name(tablename),
                query={
                    col_name: dict(
                        description=format_name(col_name),
                        schema=POSTGRES2OPENAPI.get(column.data_type, {})
                    )
                    for col_name, column in columns.items()
                },
                body=s.Object(
                    limit=s.Integer(),
                    offset=s.Integer(),
                    resolve_depth=s.Integer(),
                    columns=s.Array(s.String()),
                    filters=s.Array(
                        s.Array(
                            s.Array(
                                # s.String(), s.Number(), s.Boolean()
                            ).example(["key", "op", 'value']).size(3),
                        ),
                    ),
                    obj=s.Object({
                        col_name: dict(
                            description=format_name(col_name),
                            **POSTGRES2OPENAPI.get(column.data_type, {})
                        )
                        for col_name, column in columns.items()
                    }),
                    affected=s.Integer(),
                ).popProperties(*METHOD2POP.get(method, [])),
                responses={
                    200: s.Object({
                        col_name: POSTGRES2OPENAPI.get(column.data_type, {})
                        for col_name, column in columns.items()
                    })
                }
            )
        }
    }


def format_name(name: str):
    return re.sub(r"[-_]", ' ', name).title()

