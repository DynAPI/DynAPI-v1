#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app
try:
    import orjson
except ModuleNotFoundError:
    orjson = None


class ORJSONDecoder:

    def __init__(self, **kwargs):
        # eventually take into consideration when deserializing
        self.options = kwargs

    def decode(self, obj):
        return orjson.loads(obj)


class ORJSONEncoder:

    def __init__(self, **kwargs):
        # eventually take into consideration when serializing
        self.options = kwargs

    def encode(self, obj):
        # decode back to str, as orjson returns bytes
        return orjson.dumps(obj).decode('utf-8')


app.json_encoder = ORJSONEncoder
app.json_decoder = ORJSONDecoder
