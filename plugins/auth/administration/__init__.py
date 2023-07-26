#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""
username
password with constraints
admin-ping/debug-pin
"""
from __main__ import app
import os.path as p
import flask


admin = flask.Blueprint("administration", __name__,
                        static_folder='web/static/',
                        template_folder='web/',
                        url_prefix="/admin")


@admin.get("/")
def index():
    return flask.render_template("index.html")


@admin.get("/<path:path>")
def page(path: str):
    return flask.render_template(
        [path, p.join(path, 'index.html')],
    )


from . import crud  # noqa

app.register_blueprint(admin)
