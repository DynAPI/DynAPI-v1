#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import re


def makespec(method: str, schemaname: str, tablename: str, columns):
    columns = columns

    return {
        f'/db/{schemaname}/{tablename}': {
            f'{method}': {
                'tags': [f"{format_name(schemaname)}/{format_name(tablename)}"],
                'summary': format_name(tablename),
                # 'description': f"{method} {format_name(tablename)}",
                'parameters': [
                    {
                        'in': "query",
                        'name': col_name,
                        'schema': POSTGRES2OPENAPI.get(data_type, data_type),
                        'description': format_name(col_name),
                    }
                    for col_name, data_type in columns.items()
                ] + [
                    {
                        'in': "query",
                        'name': "__limit__",
                        'schema': {
                            'type': "number",
                        },
                        'description': "Maximum number of rows returned",
                    },
                    {
                        'in': "query",
                        'name': "__offset__",
                        'schema': {
                            'type': "number",
                        },
                        'description': "Number of rows to skip",
                    },
                    {
                        'in': "query",
                        'name': "__resolve_depth__",
                        'schema': {
                            'type': "number",
                        },
                        'description': "How deep to follow foreign keys and display the relation hierarchically",
                        # 'description': "How deep to follow foreign keys and resolve them to the right entities",
                    },
                ],
                'responses': {
                    '200': {
                        'description': "Successful operation",
                        'content': {
                            "application/json": {
                                'schema': {
                                    'type': "array",
                                    'items': {
                                        'type': "object",
                                        'properties': {
                                            col_name: POSTGRES2OPENAPI.get(data_type, data_type)
                                            for col_name, data_type in columns.items()
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }


def makespec_extra(schemaname: str, tablename: str):
    return {
        f'/db/{schemaname}/{tablename}/count': {
            f'get': {
                'tags': [f"{format_name(schemaname)}/{format_name(tablename)}"],
                'summary': f"Get count for {format_name(tablename)}",
                # 'description': f"{method} {format_name(tablename)}",
                'responses': {
                    '200': {
                        'description': "Successful operation",
                        'content': {
                            "application/json": {
                                'schema': {
                                    'type': "object",
                                    'properties': {
                                        'count': {
                                            'type': "integer"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
    }


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


def format_name(name: str):
    return re.sub(r"[-_]", ' ', name).title()
