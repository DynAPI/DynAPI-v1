#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import re
from .schema import make_schema
from . import schematypes as s


def makespec(method: str, schemaname: str, tablename: str, columns):
    return {
        f'/db/{schemaname}/{tablename}': {
            f'{method}': make_schema(
                tags=[f"{format_name(schemaname)}/{format_name(tablename)}", method.upper()],
                summary=format_name(tablename),
                query={
                    **{
                        col_name: dict(
                            description=format_name(col_name),
                            schema=POSTGRES2OPENAPI.get(column.data_type, {})
                        )
                        for col_name, column in columns.items()
                    },
                    **dict(
                        __limit__=dict(
                            description="Maximum number of rows returned",
                            schema=s.Integer(),
                        ),
                        __offset__=dict(
                            description="Number of rows to skip",
                            schema=s.Integer()
                        ),
                        __resolve_depth__=dict(
                            description="How deep to follow foreign keys and display the relation hierarchically",
                            schema=s.Integer(),
                        )
                    )
                },
                responses={
                    200: s.Object({
                        col_name: POSTGRES2OPENAPI.get(column.data_type, {})
                        for col_name, column in columns.items()
                    })
                }
            )
        }
    }


def format_name(name: str):
    return re.sub(r"[-_]", ' ', name).title()


POSTGRES2OPENAPI = {
    'bigint': dict(type='integer'),
    'bigserial': dict(type='integer'),
    'boolean': dict(type='boolean'),
    'bytea': dict(type="string", format="byte"),
    'character': dict(type="string"),
    'character varying': dict(type="string"),
    'cidr': dict(type="string", format="ipv4"),
    'date': dict(type="string", format="date"),
    'double precision': dict(type="number"),
    'inet': dict(type="string", format="ipv4"),
    'integer': dict(type='integer'),
    'json': dict(type="string"),
    'jsonb': dict(type="string", format="byte"),
    'macaddr': dict(type="string"),
    'macaddr8': dict(type="string"),
    'numeric': dict(type="number"),
    'pg_lsn': dict(type='integer'),
    'pg_snapshot': dict(type='integer'),
    'real': dict(type='number'),
    'smallint': dict(type='integer'),
    'smallserial': dict(type='integer'),
    'serial': dict(type='integer'),
    'text': dict(type='string'),
    'time': dict(type='string'),
    'tsquery': dict(type='string'),
    'tsvector': dict(type='string'),
    'txid_snapshot': dict(type='integer'),
    'uuid': dict(type='integer'),
    'xml': dict(type='string', format='xml')
}
