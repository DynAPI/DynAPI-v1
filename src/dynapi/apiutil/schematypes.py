#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import abc


class __Schema:
    _options: dict

    def __init__(self):
        self._options = {}

    def default(self, default) -> '__Schema':
        self._options["default"] = default
        return self

    def enum(self, enum: list) -> '__Schema':
        self._options["enum"] = enum
        return self

    def nullable(self, is_: bool = True) -> '__Schema':
        self._options['nullable'] = is_
        return self

    def example(self, example: str) -> '__Schema':
        self._options['example'] = example
        return self

    # @t.final
    def finalize(self) -> dict:
        return {
            attr: value
            for attr, value in {
                **self._options,
                **self._finalize(),
            }.items()
            if value is not None
        }

    @abc.abstractmethod
    def _finalize(self) -> dict:
        pass

    @staticmethod
    def _resolve_type(_type):
        if isinstance(_type, dict):
            return _type
        if _type in _builtin_types_map:
            _type = _builtin_types_map[_type]
        if callable(_type):
            _type = _type()
        return _type.finalize()


class Object(__Schema):
    def __init__(self, _props=None, **properties):
        super().__init__()
        self._properties = _props or properties

    def _finalize(self) -> dict:
        return {
            'type': "object",
            'properties': {
                attr: self._resolve_type(typ)
                for attr, typ in self._properties.items()
            }
        }


class Array(__Schema):
    # yes. type of items is not iterable
    def __init__(self, items):
        super().__init__()
        self._items = items

    def _finalize(self) -> dict:
        return {
            'type': "array",
            'items': self._resolve_type(self._items)
        }


class Integer(__Schema):
    def _finalize(self) -> dict:
        return {
            'type': "integer",
        }


class Number(__Schema):
    def _finalize(self) -> dict:
        return {
            'type': "number",
        }


class String(__Schema):
    def finalize(self) -> dict:
        return {
            'type': "string",
        }


class Boolean(__Schema):
    def _finalize(self) -> dict:
        return {
            'type': "boolean",
        }


_builtin_types_map = {
    str: String,
    bool: Boolean,
    int: Integer,
    float: Number,
}
