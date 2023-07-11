#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from .. import DatabaseConnection
from .types import TableColumn


def list_columns(connection: DatabaseConnection, schema: str, table: str) -> t.List[TableColumn]:
    cursor = connection.cursor()
    cursor.execute(r"""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = %s
    AND table_name = %s;
    """, [schema, table])
    return [
        TableColumn(
            name=row.column_name,
            data_type=row.data_type
        )
        for row in cursor.fetchall()
    ]
