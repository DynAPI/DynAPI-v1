#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app
import flask


@app.route("/redoc")
def redoc():
    return flask.render_template("redoc.html")
