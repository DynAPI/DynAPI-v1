#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""
TIP: don't ever touch this stuff, or you will get headaches
"""
import re
import http
import functools
import typing as t
import flask
from .fileconfig import config


def is_globby(pat: str) -> bool:
    return "*" in pat or "?" in pat


def translate_globby(pat: str) -> str:
    return re.escape(pat).replace(r"\*", ".*").replace(r"\?", ".")


def get_worth(pat: str):
    if pat == "?":
        return 0
    elif pat == "*":
        return 1
    elif is_globby(pat):
        return 2
    else:
        return 3


class ParsedSection:
    def __init__(self, section: str):
        self.raw = section
        parts = section.split(":")
        self.section = parts[0]
        if self.section != 'methods':
            raise KeyError(f"invalid section: {self.section!r}")
        self.schema = (parts[1] if len(parts) > 1 else None) or "*"
        self.schema_re = re.compile(translate_globby(self.schema), re.IGNORECASE) if self.schema else None
        self.table = (parts[2] if len(parts) > 2 else None) or "*"
        self.table_re = re.compile(translate_globby(self.table), re.IGNORECASE) if self.table else None

        self.worth = get_worth(self.schema) + get_worth(self.table) * 10

    def __repr__(self):
        return f"<{type(self).__name__} {self.schema}:{self.table}>"

    # used for sorting
    def __lt__(self, other: 'ParsedSection'):
        return self.worth < other.worth

    def match_schema(self, schema) -> t.Optional[bool]:
        if not self.schema:
            return None
        return self.schema_re.fullmatch(schema) is not None

    def match_table(self, table) -> t.Optional[bool]:
        if not self.table:
            return None
        return self.table_re.fullmatch(table) is not None


@functools.lru_cache()
def ordered_sections():
    return sorted(
        (ParsedSection(sec) for sec in config.sections() if sec == 'methods' or sec.startswith('methods:')),
        reverse=True
    )


@functools.lru_cache()
def method_check(*, method: str, schema: str, table: str) -> bool:
    for sec in ordered_sections():
        print(sec)
    for section in ordered_sections():
        if section.match_schema(schema) is not False and section.match_table(table) is not False:
            allowed = config.getboolean(section.raw, method, fallback=None)
            if allowed is not None:
                return allowed
    return False


def flask_method_check():
    if getattr(flask.g, 'method_checked', False):
        return
    method = flask.request.method
    schema = flask.request.view_args["schemaname"]
    table = flask.request.view_args["tablename"]
    if not method_check(method=method, schema=schema, table=table):
        # flask.abort(http.HTTPStatus.FORBIDDEN)
        flask.abort(http.HTTPStatus.METHOD_NOT_ALLOWED)
