#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import re
from database import DatabaseConnection, dbutil


def format_table_name(name: str):
    return re.sub(r"[-_]", ' ', name).title()


def makespec(connection: DatabaseConnection, method: str, schemaname: str, tablename: str):
    return {
        f'/{method}/{schemaname}/{tablename}': {
            f'{method}': {
                'tags': ["Generated"],
                'summary': f"{method}'s all information in {format_table_name(tablename)}",
                'responses': {
                    '200': {
                        'description': "Successful operation",
                        'content': {
                            "application/json": {
                                'schema': {
                                    'type': "array",
                                    'items': {
                                        'type': "object",
                                        'properties': getProperties(connection=connection, schemaname=schemaname, tablename=tablename)
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }


POSTGRES2OPENAPI = {
    'bigint': 'number',
    'integer': 'number',
    'smallint': 'number',
    'boolean': 'boolean',
    'character varying': 'string',
    'text': 'string',
}


def getProperties(connection: DatabaseConnection, schemaname: str, tablename: str):
    props = {}
    cols = dbutil.list_columns(connection=connection, schema=schemaname, table=tablename)
    for col in cols:
        props[f'{col.name}'] = {
            # 'type': col.data_type,
            'type': POSTGRES2OPENAPI.get(col.data_type, col.data_type),
        }
    return props
