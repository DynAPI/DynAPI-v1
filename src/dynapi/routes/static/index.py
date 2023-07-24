#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app, __version__
import flask
from apiconfig import config


@app.get("/")
def index():
    return flask.render_template(
        "home.html",
        docs=config.getboolean("web", "docs", fallback=False),
        swagger=config.getboolean("web", "swagger", fallback=False),
        redoc=config.getboolean("web", "redoc", fallback=False),
        version=__version__,
    )


@app.get("/favicon.ico")
def favicon():
    return flask.redirect(
        flask.url_for("static", filename="favicon.ico")
    )
