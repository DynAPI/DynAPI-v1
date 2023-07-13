#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import re
from .schema import make_schema
from . import schematypes as s
from database import POSTGRES2OPENAPI


def makespec(method: str, schemaname: str, tablename: str, columns):
    return {
        f'/api/db/{schemaname}/{tablename}': {
            f'{method}': make_schema(
                tags=[f"{format_name(schemaname)}/{format_name(tablename)}", method.upper()],
                summary=format_name(tablename),
                query={
                    **{
                        col_name: dict(
                            description=format_name(col_name),
                            schema=POSTGRES2OPENAPI.get(column.data_type, {})
                        )
                        for col_name, column in columns.items()
                    },
                    **dict(
                        __limit__=dict(
                            description="Maximum number of rows returned",
                            schema=s.Integer(),
                        ),
                        __offset__=dict(
                            description="Number of rows to skip",
                            schema=s.Integer()
                        ),
                        __resolve_depth__=dict(
                            description="How deep to follow foreign keys and display the relation hierarchically",
                            schema=s.Integer(),
                        )
                    )
                },
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

