#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app
import flask


@app.route("/swagger")
def swagger():
    return flask.render_template("swagger.html")
