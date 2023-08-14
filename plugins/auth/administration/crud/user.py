#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from flask import request
from apiutil import get_body_config
from .. import admin
import http
import base64
import typing as t
import flask
from apiconfig import config
from pypika import PostgreSQLQuery as Query, Schema, Table, Criterion, FormatParameter
from pydantic import dataclasses
from database import dbutil
from ..util.pwutil import generate_password_hash


schemaname = config.get('auth', 'schema') if config.has_option('auth', 'schema') else 'dynapi'
tablename = config.get('auth', 'users_table') if config.has_option('auth', 'users_table') else 'users'


@dataclasses.dataclass
class NewUserBody:
    username: str = dataclasses.Field(min_length=1)
    password: str = dataclasses.Field(min_length=1)
    description: t.Optional[str] = dataclasses.Field()
    roles: t.Optional[t.List[str]] = dataclasses.Field()


@admin.post("/api/user")
def create_user():
    json_body = flask.request.json
    if not isinstance(json_body, dict):
        raise flask.abort(http.HTTPStatus.BAD_REQUEST, description="body is no object")
    try:
        body = NewUserBody(**json_body)
    except (TypeError, ValueError):
        raise flask.abort(http.HTTPStatus.BAD_REQUEST)
    else:
        roles = [role.strip().lower() for role in body.roles if role.strip()]
        passwordhash = base64.b64encode(generate_password_hash(body.password.encode())).decode()
        with flask.g.db_conn as conn:
            cursor = conn.cursor()
            schema = Schema(schemaname)
            query = Query.into(schema.__getattr__(tablename)) \
                .columns("username", "passwordhash", "description", "roles") \
                .insert(body.username, passwordhash, body.description, roles) \
                .returning("*")
            cursor.execute(query)
            row = cursor.fetchone()
            conn.commit()
            return flask.jsonify({
                col.name: row[index]
                for index, col in enumerate(cursor.description)
                if col.name != "passwordhash"
            })


@admin.delete("/api/user")
def delete_users():
    if not flask.request.is_json or not isinstance(flask.request.json, dict):
        raise flask.abort(http.HTTPStatus.BAD_REQUEST)

    body = get_body_config(request)
    with flask.g.db_conn as conn:
        cursor = conn.cursor()
        schema = Schema(schemaname)
        table = Table(tablename)
        query = Query \
            .from_(schema.__getattr__(tablename)) \
            .delete() \
            .where(
                Criterion.any(
                    Criterion.all(
                        dbutil.OPMAP[op.lower()](table.__getattr__(attr), value)
                        for attr, op, value in ands
                    )
                    for ands in body.filters
                )
            ) \
            .returning("*")
        cursor.execute(query)

        conn.commit()
        return flask.jsonify([
            {col.name: row[index] for index, col in enumerate(cursor.description) if col.name != "passwordhash"}
            for row in cursor.fetchall()
        ])


@admin.put("/api/user")
def update_users():
    if not flask.request.is_json or not isinstance(flask.request.json, dict):
        raise flask.abort(http.HTTPStatus.BAD_REQUEST)

    body = get_body_config(request)
    with flask.g.db_conn as conn:
        cursor = conn.cursor()
        schema = Schema(schemaname)
        table = Table(tablename)
        query = Query \
            .update(schema.__getattr__(tablename)) \

        if "password" in body.obj:
            body.obj["passwordhash"] = base64.b64encode(generate_password_hash(body.obj["password"].encode())).decode()
            del body.obj["password"]

        for attr in body.obj.keys():
            query = query.set(table.__getattr__(attr), FormatParameter())

        query = query.where(
            Criterion.any(
                Criterion.all(
                    dbutil.OPMAP[op.lower()](table.__getattr__(attr), value)
                    for attr, op, value in ands
                )
                for ands in body.filters
            )
        )
        query = query.returning("*")

        cursor.execute(query, body.obj.values())
        conn.commit()
        return flask.jsonify([
            {col.name: row[index] for index, col in enumerate(cursor.description) if col.name != "passwordhash"}
            for row in cursor.fetchall()
        ])


@admin.get("/api/user")
def get_users():
    body = get_body_config(request)
    with flask.g.db_conn as conn:
        cursor = conn.cursor()

        schema = Schema(schemaname)
        table = Table(tablename)

        query = Query \
            .from_(schema.__getattr__(tablename)) \
            .select(*body.columns) \
            .where(
                Criterion.any(
                    Criterion.all(
                        dbutil.OPMAP[op.lower()](table.__getattr__(attr), value)
                        for attr, op, value in ands
                    )
                    for ands in body.filters
                )
            )

        if body.limit:
            query = query.limit(body.limit)
        if body.offset:
            query = query.offset(body.offset)

        cursor.execute(query)
        return flask.jsonify([
            {col.name: row[index] for index, col in enumerate(cursor.description) if col.name != "passwordhash"}
            for row in cursor.fetchall()
        ])
