#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from .. import DatabaseConnection
from .types import TableMeta


def list_tables(connection: DatabaseConnection) -> t.List[TableMeta]:
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
