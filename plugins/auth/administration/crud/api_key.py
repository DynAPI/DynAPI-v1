#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from apiutil import get_body_config
from .. import admin
import http
import secrets
import typing as t
import flask
from flask import request
from apiconfig import config
from pypika import PostgreSQLQuery as Query, Schema, Table, Criterion
from pydantic import dataclasses
from database import DatabaseConnection, dbutil


schemaname = config.get('auth', 'schema') if config.has_option('auth', 'schema') else 'dynapi'
tablename = config.get('auth', 'api_key_table') if config.has_option('auth', 'api_key_table') else 'api_keys'


@dataclasses.dataclass
class NewApiKeyBody:
    api_key: t.Optional[str] = dataclasses.Field(min_length=1)
    description: t.Optional[str] = dataclasses.Field()
    roles: t.Optional[t.List[str]] = dataclasses.Field()


@admin.route("/api_key", methods=["POST"])
def create_api_key():
    if not flask.request.is_json or not isinstance(flask.request.json, dict):
        raise flask.abort(http.HTTPStatus.BAD_REQUEST)

    try:
        body = NewApiKeyBody(**flask.request.json)
    except (TypeError, ValueError):
        raise flask.abort(http.HTTPStatus.BAD_REQUEST)
    else:
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


@admin.route("/api_key", methods=["DELETE"])
def delete_api_key():
    if not flask.request.is_json or not isinstance(flask.request.json, dict):
        raise flask.abort(http.HTTPStatus.BAD_REQUEST)

    body = get_body_config(request)
    with DatabaseConnection() as conn:
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


@admin.route("/api_key", methods=["PUT"])
def update_api_key():
    if not flask.request.is_json or not isinstance(flask.request.json, dict):
        raise flask.abort(http.HTTPStatus.BAD_REQUEST)

    body = get_body_config(request)
    with DatabaseConnection() as conn:
        from psycopg2.extras import NamedTupleCursor
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)
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


@admin.route("/api_key", methods=["GET"])
def get_api_key():
    body = get_body_config(request)
    with DatabaseConnection() as conn:
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