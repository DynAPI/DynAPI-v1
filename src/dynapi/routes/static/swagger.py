#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app
import flask
from exceptions import DoNotImportException
from apiconfig import config


if not config.getboolean("web", "swagger", fallback=False):
    raise DoNotImportException()


@app.route("/swagger", methods=["GET"])
def swagger():
    return flask.render_template("swagger.html")
