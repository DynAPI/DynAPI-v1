#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from .. import admin
from apiutil import get_body_config
import flask
from flask import request
from apiconfig import config
from pypika import PostgreSQLQuery as Query, Schema, Table, Criterion, Order
from database import dbutil


schemaname = config.get('auth', 'schema') if config.has_option('auth', 'schema') else 'dynapi'
tablename = config.get('auth', 'audit_log_table') if config.has_option('auth', 'audit_log_table') else 'audit_log'


# not starting with /api/ to prevent inserting logs
@admin.get("/audit_log")
def get_logs():
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

        if body.order_by:
            for col, asc in body.normalized_order_by:
                query = query.orderby(col, order=Order.asc if asc else Order.desc)

        cursor.execute(str(query))
        return flask.jsonify([
            {col.name: row[index] for index, col in enumerate(cursor.description)}
            for row in cursor.fetchall()
        ])
