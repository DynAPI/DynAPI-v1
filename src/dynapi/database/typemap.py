#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""

POSTGRES2OPENAPI = {
    'bigint': dict(type='integer'),
    'bigserial': dict(type='integer'),
    'bit': dict(type='string'),
    'bit varying': dict(type='string'),
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
    'time without time zone': dict(type='integer'),
    'time with time zone': dict(type='integer'),
    'timestamp without time zone': dict(type='integer'),
    'timestamp with time zone': dict(type='integer'),
    'tsquery': dict(type='string'),
    'tsvector': dict(type='string'),
    'txid_snapshot': dict(type='integer'),
    'uuid': dict(type='integer'),
    'xml': dict(type='string', format='xml')
}
