#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from collections import defaultdict
from .. import DatabaseConnection
from . import list_tables, list_columns


def list_tables_meta(connection: DatabaseConnection):
    meta_data = defaultdict(lambda: dict())
    for table in list_tables(connection=connection):
        cols = list_columns(connection=connection, schema=table.schema, table=table.table)
        meta_data[table.schema][table.table] = {
            col.name: col
            for col in cols
        }
    return meta_data
