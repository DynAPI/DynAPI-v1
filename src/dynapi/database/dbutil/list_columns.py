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
    SELECT *
    FROM information_schema.columns
    WHERE table_schema = %s
    AND table_name = %s;
    """, [schema, table])
    return [
        TableColumn(
            name=row.column_name,
            is_nullable=row.is_nullable,
            data_type=row.data_type,
            is_identity=row.is_identity,
            is_generated=row.is_generated,
            is_updatable=row.is_updatable
        )
        for row in cursor.fetchall()
    ]
