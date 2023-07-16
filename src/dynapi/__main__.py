#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
__version__ = "0.0.0"

import flask
import os.path as p
from apiconfig import config
from database import test_database_connection
import dynamic_loader as dynload


app = flask.Flask(
    __name__,
    static_folder="web",
    template_folder="web",
)

ROUTES = []
PLUGINS = []
dynload.load_folder("extra")
ROUTES.extend(dynload.load_folder("routes"))
if p.isdir("plugins"):
    PLUGINS.extend(dynload.load_plugins())


if __name__ == '__main__':
    test_database_connection()
    app.run(
        host=config.get("api", "host", fallback="localhost"),
        port=config.getint("api", "port", fallback=8080),
        debug=config.getboolean("api", "debug", fallback=False),
        threaded=config.getboolean("api", "threaded", fallback=False),
        processes=config.getint("api", "processes", fallback=1)
    )
