#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import pydantic.schema
from .schematypes import __Schema
from . import schematypes as s


def status_to_text(status: int):
    return {
        1: "Informational",
        2: "Successful Operation",
        3: "Redirect",
        4: "Bad Request",
        5: "Server Error",
    }.get(status // 100, "Unknown Operation")


def make_schema(
        *,
        tags: t.List[str] = None,
        summary: str = None,
        path: t.Dict[str, dict] = None,
        query: t.Dict[str, dict] = None,
        body: __Schema = None,
        responses: t.Dict[int, __Schema] = None,
        add_default_responses: bool = True
):
    def resolve(schema):
        return schema.finalize() if hasattr(schema, 'finalize') else schema

    if add_default_responses:
        responses = {
            500: s.Object(
                type=s.String(),
                detail=s.String(),
            ),
            **responses
        }

    return dict(
        tags=tags or [],
        summary=summary,
        parameters=[
            *[{'in': "path", 'name': name, **q, 'schema': resolve(q['schema'])} for name, q in (path or {}).items()],
            *[{'in': "query", 'name': name, **q, 'schema': resolve(q['schema'])} for name, q in (query or {}).items()],
        ],
        requestBody=dict(
            content={
                'application/json': {
                    'schema': resolve(body)
                },
            }
        ),
        responses={
            str(status): {
                'description': status_to_text(status),
                'content': {
                    "application/json": {
                        'schema': resolve(schema)
                    }
                }
            }
            for status, schema in responses.items()
        }
    )


def get_model_schema(cls):
    schema = pydantic.schema.model_schema(cls, by_alias=False)
    definitions = schema.pop('definitions')
    replace_with_definitions(schema['properties'], definitions)
    return schema


def replace_with_definitions(obj, definitions):
    for attr, scheme in obj.items():
        ref = scheme.get("$ref")
        if ref:
            obj[attr] = scheme = definitions[ref.rsplit("/", 1)[1]]
        if scheme.get('type') == "object":
            replace_with_definitions(scheme['properties'], definitions)

