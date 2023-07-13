#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from .. import DatabaseConnection
from .types import Constraints


def get_constraints(connection: DatabaseConnection, schema: str, table: str) -> t.List[Constraints]:
    cursor = connection.cursor()
    cursor.execute(r"""
    SELECT tc.constraint_name, tc.constraint_type, ccu.table_name as referenced_table_name, ccu.column_name as referenced_column_name, c.data_type, c.is_updatable
    FROM information_schema.table_constraints tc 
    JOIN information_schema.constraint_column_usage AS ccu USING (constraint_schema, constraint_name) 
    JOIN information_schema.columns AS c ON c.table_schema = tc.constraint_schema
    AND tc.table_name = c.table_name AND ccu.column_name = c.column_name
    WHERE (constraint_type = 'PRIMARY KEY' OR constraint_type = 'FOREIGN KEY') and tc.table_name = 'inventory_system';;
    """, [schema, table])

    tableConstraints = [ Constraints(
        constraint_name=row.constraint_name,
        constraint_type=row.constraint_type,
        referenced_table_name=row.referenced_table_name,
        referenced_column_name=row.referenced_column_name,
        data_type=row.data_type,
        is_updatable=row.is_updatable
    )
    for row in cursor.fetchall() ]

    cursor.execute(r"""
    """, [schema, table])

    viewConstraints = [Constraints(
        constraint_name=row.constraint_name,
        constraint_type=row.constraint_type,
        referenced_table_name=row.referenced_table_name,
        referenced_column_name=row.referenced_column_name,
        data_type=row.data_type,
        is_updatable=row.is_updatable
    )
        for row in cursor.fetchall()]

    return tableConstraints + viewConstraints