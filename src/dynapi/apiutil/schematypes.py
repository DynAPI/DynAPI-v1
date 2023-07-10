#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import abc


class __Schema:
    _options: dict

    def __init__(self):
        self._options = {}

    def nullable(self, is_: bool = True) -> '__Schema':
        self._options['nullable'] = is_
        return self

    def example(self, *, example: str) -> '__Schema':
        self._options['example'] = example
        return self

    @abc.abstractmethod
    def finalize(self) -> dict:
        pass

    @staticmethod
    def _resolve_type(_type):
        if _type in _builtin_types_map:
            _type = _builtin_types_map[_type]
        if callable(_type):
            _type = _type()
        return _type.finalize()


class Object(__Schema):
    def __init__(self, _props=None, **properties):
        super().__init__()
        self._properties = _props or properties

    def finalize(self) -> dict:
        return {
            'type': "object",
            **self._options,
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

    def finalize(self) -> dict:
        return {
            'type': "array",
            **self._options,
            'items': self._resolve_type(self._items)
        }


class Integer(__Schema):
    def finalize(self) -> dict:
        return {
            'type': "integer",
            **self._options,
        }


class Number(__Schema):
    def finalize(self) -> dict:
        return {
            'type': "number",
            **self._options,
        }


class String(__Schema):
    def finalize(self) -> dict:
        return {
            'type': "string",
            **self._options,
        }


class Boolean(__Schema):
    def finalize(self) -> dict:
        return {
            'type': "boolean",
            **self._options,
        }


_builtin_types_map = {
    str: String,
    bool: Boolean,
    int: Integer,
    float: Number,
}
