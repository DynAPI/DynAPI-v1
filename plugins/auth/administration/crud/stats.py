#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from .. import admin
import flask


@admin.get("/api/stats")
def count_stats():
    with flask.g.db_conn as conn:
        cursor = conn.cursor()
        cursor.execute(r"""
        SELECT  (
            SELECT COUNT(*)
            FROM dynapi.users
        ) AS users_count,
        (
            SELECT COUNT(*)
            FROM dynapi.api_keys
        ) AS api_keys_count,
        (
            SELECT COUNT(*)
            FROM dynapi.audit_log
        ) AS audit_logs_count
        """)
        row = cursor.fetchone()
        return flask.jsonify({
            col.name: row[index] for index, col in enumerate(cursor.description)
        })
