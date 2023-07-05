#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import flask
from __main__ import app
from database import DatabaseConnection
from pypika import PostgreSQLQuery as Query, Schema, Table


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
