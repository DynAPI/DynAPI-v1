#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from .. import admin
import http
import secrets
import typing as t
import flask
from pypika import PostgreSQLQuery as Query, Schema
from pydantic import dataclasses
from database import DatabaseConnection


@dataclasses.dataclass
class NewApiKeyBody:
    api_key: t.Optional[str] = dataclasses.Field(min_length=1)
    description: t.Optional[str] = dataclasses.Field()
    roles: t.Optional[t.List[str]] = dataclasses.Field()


@admin.route("/create/api_key", methods=["POST"])
def create_api_key():
    if not flask.request.is_json or not isinstance(flask.request.json, dict):
        raise flask.abort(http.HTTPStatus.BAD_REQUEST)

    try:
        body = NewApiKeyBody(**flask.request.json)
    except (TypeError, ValueError):
        raise flask.abort(http.HTTPStatus.BAD_REQUEST)
    else:
        schemaname, tablename = 'dynapi', 'api_keys'
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            schema = Schema(schemaname)
            query = Query.into(schema.__getattr__(tablename)) \
                .columns("api_key", "description", "roles") \
                .insert(body.api_key or secrets.token_hex(), body.description, body.roles) \
                .returning("*")
            cursor.execute(str(query))
            row = cursor.fetchone()
            conn.commit()
            return flask.jsonify({
                col.name: row[index]
                for index, col in enumerate(cursor.description)
            })
