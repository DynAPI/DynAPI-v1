#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from .. import DatabaseConnection
from .types import Count as CountType
from pypika import PostgreSQLQuery as Query, Schema
from pypika.functions import Count


def get_count(connection: DatabaseConnection, schema: str, table: str) -> Count:
    cursor = connection.cursor()
    query = Query.from_(Schema(schema).__getattr__(table)).select(Count("*"))
    cursor.execute(str(query))

    row = cursor.fetchone()

    return CountType(count=row.count)
