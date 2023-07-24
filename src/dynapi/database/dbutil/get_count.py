#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import flask
from pypika import PostgreSQLQuery as Query, Schema
from pypika.functions import Count
from .types import Count as CountType


def get_count(schema: str, table: str, connection=None) -> Count:
    connection = connection or flask.g.db_conn

    cursor = connection.cursor()
    query = Query.from_(Schema(schema).__getattr__(table)).select(Count("*"))
    cursor.execute(str(query))

    row = cursor.fetchone()

    return CountType(count=row.count)
