#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import flask
from flask import request
from __main__ import app
from database import DatabaseConnection


@app.route("/list-tables-meta")
def list_tables_meta():
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(r"""
        SELECT nspname
        FROM pg_catalog.pg_namespace
        """)
        meta_data = {
            row.nspname: {}
            for row in cursor.fetchall()
        }
        for schema_name, schema_meta in meta_data.items():
            cursor.execute(r"""
                    SELECT schemaname, tablename, tableowner
                    FROM pg_catalog.pg_tables
                    WHERE schemaname = %s
                    """, [schema_name])
            for row in cursor.fetchall():
                schema_meta[row.tablename] = {}
            for table_name, table_meta in schema_meta.items():
                cursor.execute(r"""
                        SELECT *
                        FROM information_schema.columns
                        WHERE table_schema = %s
                        AND table_name = %s;
                        """, [schema_name, table_name])
                for row in cursor.fetchall():
                    table_meta[row.column_name] = dict(
                        is_nullable=row.is_nullable,
                        data_type=row.data_type,
                        is_identity=row.is_identity,
                        is_generated=row.is_generated,
                        is_updatable=row.is_updatable
                    )

        response_format = request.args.get('format', 'short')
        if response_format == "short":
            return flask.jsonify(meta_data)
        elif response_format == "long":
            return flask.jsonify([
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
                } for schema_name, table_meta in meta_data.items()
            ])
        else:
            raise KeyError(response_format)


def get_openapi_spec():
    def get_basic_meta(schema: dict, fmt: str):
        return {
            'get': {
                'tags': ["Meta"],
                'summary': f"Gets Schema with their Tables and columns ({fmt})",
                'parameters': [
                    {
                        'name': "__format__",
                        'in': "query",
                        'description': "Response Format",
                        'schema': dict(
                            type="string",
                            enum=["short", "long"],
                            default="short",
                            example=fmt,
                        )
                    },
                ],
                'responses': {
                    '200': {
                        'description': "Successful operation",
                        'content': {
                            "application/json": {
                                'schema': schema
                            }
                        }
                    }
                }
            }
        }

    return {
        # format: A
        # {
        #     schema: {
        #         table: {
        #             id: {},
        #             name: {}
        #         },
        #     },
        # }
        '/list-tables-meta': get_basic_meta({
            'type': "object",
            'properties': {
                'schema': {
                    'type': "object",
                    'properties': {
                        'table': {
                            'type': "object",
                            'properties': {
                                'column': {
                                    'type': "object",
                                    'properties': {
                                        'is_nullable': {
                                            'type': "string"
                                        },
                                        'data_type': {
                                            'type': "string"
                                        },
                                        'is_identity': {
                                            'type': "string"
                                        },
                                        'is_generated': {
                                            'type': "string"
                                        },
                                        'is_updatable': {
                                            'type': "string"
                                        },
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }, "short"),
        # format: B
        # [
        #     {
        #         schema_name: string,
        #         tabels: [
        #             {
        #                 table_name: string
        #                 columns: [
        #                     {
        #                         column_name: string
        #                     }
        #                 ]
        #             }
        #         ]
        #     }
        # ]
        '/list-tables-meta?__format__=long': get_basic_meta({
            'type': "array",
            'items': {
                'type': "object",
                'properties': {
                    'schema_name': {
                        'type': "string",
                    },
                    'tables': {
                        'type': "array",
                        'items': {
                            'type': "object",
                            'properties': {
                                'table_name': {
                                    'type': "string",
                                },
                                'columns': {
                                    'type': "array",
                                    'items': {
                                        'type': "object",
                                        'properties': {
                                            'is_nullable': {
                                                'type': "string"
                                            },
                                            'data_type': {
                                                'type': "string"
                                            },
                                            'is_identity': {
                                                'type': "string"
                                            },
                                            'is_generated': {
                                                'type': "string"
                                            },
                                            'is_updatable': {
                                                'type': "string"
                                            },
                                        }
                                    }
                                }
                            },
                        }
                    }
                },
            }
        }, "long")
    }
