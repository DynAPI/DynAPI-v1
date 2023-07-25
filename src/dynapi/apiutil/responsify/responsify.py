#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app
try:
    import orjson as json
except ModuleNotFoundError:
    import json
import re
import flask
import psycopg2 as psql
import psycopg2.extensions
from .convert2default import convert2default
from .register import converters


mime_split = re.compile(r'\s*;\s*')


def responsify(*args, **kwargs):
    if args and kwargs:
        raise TypeError("responsify() behavior undefined when passed both args and kwargs")
    elif len(args) == 1:  # single args are passed directly to dumps()
        data = args[0]
    else:
        data = args or kwargs

    data = prepare_data(data)

    for accept in mime_split.split(flask.request.headers.get("Accept")):
        if accept in converters:
            dumped, mimetype = converters[accept](data)
            break
    else:
        dumped, mimetype = default_converter(data)

    return app.response_class(dumped, mimetype=mimetype)


def prepare_data(data):
    if isinstance(data, psql.extensions.cursor):
        return cursor2data(cursor=data)
    return data


def default_converter(data):
    return json.dumps(data, default=convert2default), "application/json"


def cursor2data(cursor: psql.extensions.cursor):
    return [
        {col.name: row[index] for index, col in enumerate(cursor.description)}
        for row in cursor.fetchall()
    ]
    # def cursor_iter():
    #     while True:
    #         rows = cursor.fetchmany(1_000)
    #         print("Yield", len(rows))
    #         if not rows:
    #             break
    #         yield from (
    #             {col.name: row[index] for index, col in enumerate(cursor.description)}
    #             for row in rows
    #         )
    # return FakeListIterator(cursor_iter())
