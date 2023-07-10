#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import uuid
import decimal
import dataclasses
from datetime import date
import flask
from werkzeug.http import http_date
try:
    import msgpack
except ModuleNotFoundError:
    msgpack = None


flask_jsonify = flask.jsonify


def msgpack_default(o):
    # this function is similar/identical to flask.json.JsonEncoder.default(self, o)
    if isinstance(o, date):
        return http_date(o)
    if isinstance(o, (decimal.Decimal, uuid.UUID)):
        return str(o)
    if dataclasses.is_dataclass(o):
        return dataclasses.asdict(o)
    if hasattr(o, "__html__"):
        return str(o.__html__())
    raise TypeError(f"Object of type '{type(o).__name__}' is not JSON serializable")


def msgpack_jsonify(*args, **kwargs):
    accept_mimetypes = flask.request.accept_mimetypes
    if 'application/msgpack' in accept_mimetypes or 'application/x-msgpack' in accept_mimetypes:
        if args and kwargs:
            raise TypeError("jsonify() behavior undefined when passed both args and kwargs")
        elif len(args) == 1:  # single args are passed directly to dumps()
            data = args[0]
        else:
            data = args or kwargs

        return flask.current_app.response_class(
            f"{msgpack.dumps(data, default=msgpack_default)}\n",
            mimetype="application/msgpack",
        )
    return flask_jsonify(*args, **kwargs)


def install():
    if msgpack:
        flask.jsonify = msgpack_jsonify
    return msgpack is not None
