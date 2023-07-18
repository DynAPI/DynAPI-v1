#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from .. import admin
import http
import base64
import typing as t
import flask
from pypika import PostgreSQLQuery as Query, Schema, Table
from pydantic import dataclasses
from database import DatabaseConnection
from .pwutil import generate_password_hash


@dataclasses.dataclass
class NewUserBody:
    username: str = dataclasses.Field(min_length=1)
    password: str = dataclasses.Field(min_length=1)
    description: t.Optional[str] = dataclasses.Field()
    roles: t.Optional[t.List[str]] = dataclasses.Field()


@admin.route("/create/user", methods=["POST"])
def create_user():
    try:
        body = NewUserBody(**flask.request.json)
    except (TypeError, ValueError):
        raise flask.abort(http.HTTPStatus.BAD_REQUEST)
    else:
        passwordhash = base64.b64encode(generate_password_hash(body.password.encode())).decode()
        schemaname, tablename = 'dynapi', 'users'
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            schema = Schema(schemaname)
            query = Query.into(schema.__getattr__(tablename)) \
                .columns("username", "passwordhash", "description", "roles") \
                .insert(body.username, passwordhash, body.description, body.roles) \
                .returning("*")
            cursor.execute(str(query))
            row = cursor.fetchone()
            conn.commit()
            return flask.jsonify({
                col.name: row[index]
                for index, col in enumerate(cursor.description)
                if col.name != "passwordhash"
            })
