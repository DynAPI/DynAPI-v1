#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import abc
import typing as t


class __Schema:
    _options: dict

    def __init__(self):
        self._options = {}

    def __getitem__(self, item):
        return self._options[item]

    def __setitem__(self, key, value):
        self._options[key] = value

    def description(self, default) -> '__Schema':
        self["description"] = default
        return self

    def default(self, default) -> '__Schema':
        self["default"] = default
        return self

    def enum(self, enum: list) -> '__Schema':
        self["enum"] = enum
        return self

    def nullable(self, is_: bool = True) -> '__Schema':
        self['nullable'] = is_
        return self

    def example(self, example: t.Union[str, t.List[str]]) -> '__Schema':
        self['example'] = example
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


class AnyType(__Schema):
    def _finalize(self) -> dict:
        return {
            'AnyValue': '{}',
        }


class Object(__Schema):
    def __init__(self, _props=None, **properties):
        super().__init__()
        self._properties = _props or properties

    def required(self, *props):
        self["required"] = props
        return self

    def minProperties(self, value: int):
        self["minProperties"] = value
        return self

    def maxProperties(self, value: int):
        self["maxProperties"] = value
        return self

    def popProperties(self, *props: t.List[str]) -> 'Object':
        if len(props) == 1 and isinstance(props[0], (list, tuple)):
            props = props[0]
        return Object({
            prop: value
            for prop, value in self._properties.items()
            if prop not in props
        })

    def _finalize(self) -> dict:
        if not self._properties:
            return {'type': "object"}

        return {
            'type': "object",
            'properties': {
                attr: self._resolve_type(typ)
                for attr, typ in self._properties.items()
            }
        }

    def debugPrint(self):
        print(self._properties)
        print(self.finalize())
        return self


class Array(__Schema):
    # yes. type of items is not iterable
    def __init__(self, *items):
        super().__init__()
        self._items = items

    def size(self, value: int):
        self["minItems"] = value
        self["maxItems"] = value
        return self

    def minSize(self, value: int):
        self["minItems"] = value
        return self

    def maxSize(self, value: int):
        self["maxItems"] = value
        return self

    def uniqueItems(self, is_: bool = True):
        self["uniqueItems"] = is_
        return self

    def _resolved_items(self):
        if not self._items:
            return '{}'  # 'items: {}' is a wildcard
        if len(self._items) == 1:
            return self._resolve_type(self._items[0])
        return dict(
            anyOf=[self._resolve_type(item) for item in self._items]
        )

    def _finalize(self) -> dict:
        return {
            'type': "array",
            'items': self._resolved_items()
        }


class Integer(__Schema):
    def ge(self, value: int):
        self["minimum"] = value
        self["exclusiveMinimum"] = False
        return self

    def gt(self, value: int):
        self["minimum"] = value
        self["exclusiveMinimum"] = True
        return self

    def le(self, value: int):
        self["maximum"] = value
        self["exclusiveMaximum"] = False
        return self

    def lt(self, value: int):
        self["maximum"] = value
        self["exclusiveMaximum"] = True
        return self

    def _finalize(self) -> dict:
        return {
            'type': "integer",
        }


class Number(__Schema):
    def ge(self, value: float):
        self["minimum"] = value
        self["exclusiveMinimum"] = False
        return self

    def gt(self, value: float):
        self["minimum"] = value
        self["exclusiveMinimum"] = True
        return self

    def le(self, value: float):
        self["maximum"] = value
        self["exclusiveMaximum"] = False
        return self

    def lt(self, value: float):
        self["maximum"] = value
        self["exclusiveMaximum"] = True
        return self

    def _finalize(self) -> dict:
        return {
            'type': "number",
        }


class String(__Schema):
    def minLength(self, value: int):
        self["minLength"] = value
        return self

    def maxLength(self, value: int):
        self["maxLength"] = value
        return self

    def format(self, fmt: str):
        self["format"] = fmt
        return self

    def pattern(self, pattern: str):
        self["pattern"] = pattern
        return self

    def _finalize(self) -> dict:
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
