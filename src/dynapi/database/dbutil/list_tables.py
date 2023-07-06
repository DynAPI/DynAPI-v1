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
    return [
        TableMeta(
            schema=row.schemaname,
            table=row.tablename,
            owner=row.tableowner,
        )
        for row in cursor.fetchall()
    ]
