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
from pypika import PostgreSQLQuery as Query, Schema, Table, Criterion
from pydantic import dataclasses
from database import DatabaseConnection, dbutil
from .pwutil import generate_password_hash

schemaname = config.get('auth', 'schema') if config.has_option('auth', 'schema') else 'dynapi'
tablename = config.get('auth', 'users_table') if config.has_option('auth', 'users_table') else 'users'


@dataclasses.dataclass
class NewUserBody:
    username: str = dataclasses.Field(min_length=1)
    password: str = dataclasses.Field(min_length=1)
    description: t.Optional[str] = dataclasses.Field()
    roles: t.Optional[t.List[str]] = dataclasses.Field()


@admin.post("/api/user")
def create_users():
    try:
        body = NewUserBody(**flask.request.json)
    except (TypeError, ValueError):
        raise flask.abort(http.HTTPStatus.BAD_REQUEST)
    else:
        roles = [role.lower() for role in body.roles]
        passwordhash = base64.b64encode(generate_password_hash(body.password.encode())).decode()
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            schema = Schema(schemaname)
            query = Query.into(schema.__getattr__(tablename)) \
                .columns("username", "passwordhash", "description", "roles") \
                .insert(body.username, passwordhash, body.description, roles) \
                .returning("*")
            cursor.execute(str(query))
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
        cursor.execute(str(query))

        conn.commit()
        return flask.jsonify([
            {col.name: row[index] for index, col in enumerate(cursor.description)}
            for row in cursor.fetchall()
        ])


@admin.put("/api/user")
def update_users():
    if not flask.request.is_json or not isinstance(flask.request.json, dict):
        raise flask.abort(http.HTTPStatus.BAD_REQUEST)

    body = get_body_config(request)
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        schema = Schema(schemaname)
        table = Table(tablename)
        query = Query \
            .update(schema.__getattr__(tablename)) \

        for attr, value in body.obj.items():
            query = query.set(table.__getattr__(attr), value)

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
        print(query)
        cursor.execute(str(query))
        conn.commit()
        return flask.jsonify([
            {col.name: row[index] for index, col in enumerate(cursor.description)}
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
            query = query.limit(body.limit).offset(body.offset)

        cursor.execute(str(query))
        return flask.jsonify([
            {col.name: row[index] for index, col in enumerate(cursor.description)}
            for row in cursor.fetchall()
        ])
