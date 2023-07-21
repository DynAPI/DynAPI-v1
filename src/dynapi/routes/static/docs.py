#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""
https://stackoverflow.com/questions/6656363/proxying-to-another-web-service-with-flask
"""
from __main__ import app
import flask
from exceptions import DoNotImportException
from apiconfig import config


if not config.getboolean("web", "docs", fallback=False):
    raise DoNotImportException()


@app.route("/docs/", methods=["GET"])
def docs():
    return flask.redirect("https://dynapi-docs.readthedocs.io/en/latest/")
