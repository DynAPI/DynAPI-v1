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


dirpath = p.dirname(__file__)
admin = flask.Blueprint("administration", __name__,
                        static_folder='web/static/',
                        template_folder='web/',
                        url_prefix="/admin")


@admin.route("/", methods=["GET"])
def index():
    return flask.render_template(
        "index.html",
    )


@admin.route("/favicon.ico", methods=["GET"])
def favicon():
    return flask.redirect(
        flask.url_for("static", filename="favicon.ico")
    )


from . import crud  # noqa

app.register_blueprint(admin)
