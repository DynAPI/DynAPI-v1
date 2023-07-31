#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from .. import admin
from __main__ import PLUGINS
import flask


@admin.get("/api/list-plugins")
def list_plugins():
    return flask.jsonify(list(PLUGINS.keys()))


@admin.get("/api/plugin-status/<string:name>")
def plugin_status(name: str):
    return {'status': "active" if name in PLUGINS else "inactive"}
