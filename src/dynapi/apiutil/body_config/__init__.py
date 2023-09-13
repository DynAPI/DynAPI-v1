#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import http
import json
import typing as t
from werkzeug.exceptions import BadRequest
import flask
from pydantic import dataclasses


@dataclasses.dataclass
class BodyConfig:
    limit: int = dataclasses.Field(None, gt=0)
    offset: int = dataclasses.Field(None, ge=0)
    # resolve_depth: int = dataclasses.Field(default=0, ge=0, le=10)
    columns: t.List[str] = dataclasses.Field(default_factory=lambda: ["*"])
    filters: t.List[t.List[t.Tuple[str, str, t.Union[bool, int, float, str]]]] = dataclasses.Field(default_factory=list)
    obj: dict = dataclasses.Field(None)
    # objects: t.List[dict] = dataclasses.Field(None)
    affected: t.Union[int, t.Tuple[int, int]] = dataclasses.Field(None)
    # group_by: t.Union[str, t.List[str]] = dataclasses.Field(None)
    # having: ...
    order_by: t.Union[str, t.Tuple[str, bool], t.List[t.Union[str, t.Tuple[str, bool]]]] = dataclasses.Field(None)

    @property
    def normalized_order_by(self) -> t.Optional[t.List[t.Tuple[str, bool]]]:
        if isinstance(self.order_by, str):
            return [(self.order_by, True)]
        elif isinstance(self.order_by, (list, tuple)):
            if len(self.order_by) == 2 and isinstance(self.order_by[1], bool):
                return [self.order_by]
            else:
                return [
                    [ob, True] if isinstance(ob, str) else ob
                    for ob in self.order_by
                ]
        else:
            return None


def get_body_config(request: flask.Request) -> BodyConfig:
    conf: t.Dict[str, t.Any] = {}
    extra_filter = []
    if request.args:
        for attr, value in request.args.items():
            if attr.startswith("__") and attr.endswith("__"):
                try:
                    conf[attr[2:-2]] = json.loads(value)
                except json.JSONDecodeError:
                    conf[attr[2:-2]] = value
            else:
                extra_filter.append((attr, "==", value))
    if request.is_json:
        conf.update(request.json)
    elif request.mimetype:
        raise flask.abort(
            code=http.HTTPStatus.BAD_REQUEST,
            description="Body is not JSON",
        )
    conf.setdefault('filters', [])
    if extra_filter:
        conf['filters'].append(extra_filter)
    try:
        return BodyConfig(**conf)
    except TypeError as exc:
        raise BadRequest(description=str(exc))
