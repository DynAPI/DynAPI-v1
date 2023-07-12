#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import http
import typing as t
import flask
from pydantic import dataclasses


@dataclasses.dataclass
class BodyConfig:
    limit: int = dataclasses.Field(default=1000, gt=0, le=1000)
    offset: int = dataclasses.Field(default=0, ge=0)
    resolve_depth: int = dataclasses.Field(default=0, ge=0, le=10)
    columns: t.List[str] = dataclasses.Field(default_factory=lambda: ["*"])
    filters: t.List[t.List[t.Tuple[str, str, t.Union[bool, int, float, str]]]] = dataclasses.Field(default_factory=list)
    obj: dict = dataclasses.Field(None)
    affected: t.Union[int, t.Tuple[int, int]] = dataclasses.Field(None)
    # objects: t.List[dict] = dataclasses.Field(None)


def get_body_config(request: flask.Request) -> BodyConfig:
    if not request.is_json:
        flask.abort(http.HTTPStatus.BAD_REQUEST)
    conf = BodyConfig(**(request.json or {}))
    if request.args:
        conf.filters.append([
            (col, "==", value)
            for col, value in request.args.items()
            if not col.startswith("__") and not col.endswith("__")
        ])
    return conf
