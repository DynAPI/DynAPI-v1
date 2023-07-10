#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import typing as t


TYPE_MAP = {
    int: "integer",
    float: "number",
    bool: "boolean",
    str: "string",
    # tuple: "array",
    # list: "array",
    # object: "object"
}


def class2schema(cls):
    return {
        'type': "object",
        'properties': class2props(cls)
    }


def class2props(cls):
    props = {}
    # print(cls.__annotations__)
    for attr, pycls in cls.__annotations__.items():
        if pycls.__module__ == "typing":
            origin = pycls.__origin__
            if origin in [t.List, t.Tuple]:
                typ = TYPE_MAP.get(pycls.__args__[0])
                if not typ:
                    props[attr] = {
                        'type': "array",
                        'items': {
                            'type': "object",
                            'properties': class2schema(pycls.__args__[0])
                        }
                    }
                else:
                    props[attr] = {
                        'type': "array",
                        'items': {
                            'type': typ
                        }
                    }
            continue
        typ = TYPE_MAP.get(pycls)
        if not typ:
            props[attr] = {
                'type': "object",
                'properties': class2schema(pycls)
            }
            continue
        props[attr] = {
            'type': typ,
        }
    return props


if __name__ == '__main__':
    from dataclasses import dataclass
    import json

    tl = t.List[int]
    print(vars(tl))
    tt = t.Tuple[str, str, str]
    print(tt.__args__)

    # __origin__: typing.List[int]
    # __extra__: list
    # __args__: int

    class SubTest:
        name: str

    @dataclass()
    class Test:
        id: int
        name: str
        arr: t.List[int]
        sub: t.List[SubTest]

    schema = class2schema(Test)
    print(json.dumps(schema, indent=2))
