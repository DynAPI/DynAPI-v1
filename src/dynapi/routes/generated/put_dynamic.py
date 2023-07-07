#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app
from database import DatabaseConnection, dbutil
from util import makespec
from exceptions import DoNotImportException
from apiconfig import config


if not config.getboolean("methods", "put", fallback=False):
    raise DoNotImportException()


def get_openapi_spec(connection: DatabaseConnection, tables_meta):
    spec = {}
    for table in dbutil.list_tables(connection=connection):
        spec.update(
            makespec(method="put", schemaname=table.schema, tablename=table.table,
                     columns=tables_meta[table.schema][table.table])
        )
    return spec
