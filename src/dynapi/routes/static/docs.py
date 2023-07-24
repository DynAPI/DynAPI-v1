#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""
This is not an offline documentation

https://stackoverflow.com/questions/6656363/proxying-to-another-web-service-with-flask
"""
from __main__ import app
import os.path as p
import flask
from exceptions import DoNotImportException
from apiconfig import config


if not config.getboolean("web", "docs", fallback=False):
    raise DoNotImportException()


@app.get("/docs/")
@app.get("/docs/<path:path>")
def docs(*_, **__):
    fp = flask.request.path
    fp = fp[1:] if fp.startswith("/") else fp
    fp = p.join(app.static_folder, fp)
    fp = p.join(fp, "index.html") if p.isdir(fp) else fp
    fp = p.relpath(fp, app.static_folder)
    return flask.send_from_directory(app.static_folder, fp)
