#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app
import dataclasses
import flask.json.tag


class TagDataClasses(flask.json.tag.JSONTag):
    __slots__ = ('serializer',)
    # key = ' dc'

    def check(self, value):
        return dataclasses.is_dataclass(value)

    def to_json(self, value):
        return value.asdict()

    # def to_python(self, value):
    #     pass


app.session_interface.serializer.register(TagDataClasses)
