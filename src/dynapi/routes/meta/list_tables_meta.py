#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import flask
from flask import request
from __main__ import app
from database import dbutil
from apiutil import make_schema, responsify, schematypes as s


@app.route("/api/list-tables-meta", methods=["OPTIONS"])
def list_tables_meta():
    meta_data = dbutil.list_tables_meta()

    response_format = request.args.get('format', 'short')
    if response_format == "short":
        return responsify(meta_data)
    elif response_format == "long":
        return responsify(
            transform_format_short2long(meta_data)
        )
    else:
        raise KeyError(response_format)


def transform_format_short2long(short):
    return [
        {
            'schema_name': schema_name,
            'tables': [
                {
                    'table_name': table_name,
                    'columns': [
                        {
                            'column_name': column_name,
                            'specs': cols
                        } for column_name, cols in column_meta.items()
                    ]
                } for table_name, column_meta in table_meta.items()
            ]
        } for schema_name, table_meta in short.items()
    ]


def get_openapi_spec(_):
    return {
        '/api/list-tables-meta': {
            'options': make_schema(
                tags=["Meta"],
                summary="Gets Schema with their Tables and columns (short)",
                query=dict(
                    __format__=dict(
                        description="Format of tables-meta",
                        schema=s.String()
                        .enum(["short", "long"])
                        .default("short")
                        .example("long")
                    )
                ),
                responses={
                    200: s.Object({
                        '[schema]': s.Object({
                            '[table]': s.Object({
                                '[column]': s.Object(
                                    name=s.String(),
                                    data_type=s.String(),
                                )
                            })
                        })
                    }),
                }
            ),
        },
        '/api/list-tables-meta?__format__=long': {
            'options': make_schema(
                tags=["Meta"],
                summary="Gets Schema with their Tables and columns (short)",
                query=dict(
                    __format__=dict(
                        description="Format of tables-meta",
                        schema=s.String()
                        .enum(["short", "long"])
                        .default("short")
                        .example("long")
                    )
                ),
                responses={
                    200: s.Array(
                        s.Object(
                            schema_name=s.String(),
                            tables=s.Array(
                                s.Object(
                                    table_name=s.String(),
                                    columns=s.Array(
                                        s.Object(
                                            column_name=s.String(),
                                            specs=s.Object(
                                                name=s.String(),
                                                data_type=s.String(),
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    ),
                }
            ),
        }
    }
