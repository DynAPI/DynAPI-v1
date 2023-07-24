#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import flask
from .types import TableMeta


def list_tables(connection=None) -> t.List[TableMeta]:
    connection = connection or flask.g.db_conn

    cursor = connection.cursor()
    # TODO: dynamic where depending on api.conf
    cursor.execute(r"""
    SELECT schemaname, tablename, tableowner
    FROM pg_catalog.pg_tables
    WHERE schemaname != 'information_schema' AND schemaname != 'pg_catalog'
    """)
    tables = [
        TableMeta(
            schema=row.schemaname,
            table=row.tablename,
            type="table",
        )
        for row in cursor.fetchall()
    ]
    cursor.execute(r"""
    select
    table_schema as schemaname, table_name as tablename
    from INFORMATION_SCHEMA.views
    WHERE
    table_schema != 'information_schema'
    AND
    table_schema != 'pg_catalog'
     """)
    views = [
        TableMeta(
            schema=row.schemaname,
            table=row.tablename,
            type="view",
        )
        for row in cursor.fetchall()
    ]
    return tables + views
