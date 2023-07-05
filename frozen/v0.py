#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import flask
from flask import request
from apiconfig import config
from database import DatabaseConnection
from pypika import PostgreSQLQuery as Query, Schema, Table, Column


app = flask.Flask(
    __name__,
    static_folder="web",
    template_folder="web",
)


# @app.errorhandler(Exception)
def error_handler(error: Exception):
    return dict(
        type=type(error).__name__,
        detail=str(error),
    )


@app.route("/", methods=["GET"])
def index():
    return {"Hello": "World"}


import routes.static.redoc
import routes.static.swagger
import routes.static.openapi

import routes.meta.list_tables_meta
import routes.meta.list_tables
import routes.meta.list_columns


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

        # format: A
        # {
        #     schema: {
        #         table: {
        #             id: {},
        #             name: {}
        #         },
        #     },
        # }
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


@app.route("/select/<string:schema>/<string:table>")
def select(schema: str, table: str):
    with DatabaseConnection() as conn:
        from psycopg2.extras import NamedTupleCursor
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)

        schema = Schema(schema)

        query = Query\
            .from_(schema.__getattr__(table))\
            .select("*")

        table = Table(table)

        for column, value in request.args.items():
            query = query.where(table.__getattr__(column) == value)

        print(query)

        cursor.execute(str(query))
        return flask.jsonify([
            {col.name: row[index] for index, col in enumerate(cursor.description)}
            for row in cursor.fetchall()
        ])


if __name__ == '__main__':
    app.run(
        host=config.get("api", "host"),
        port=config.getint("api", "port"),
        debug=config.getboolean("api", "debug"),
    )
