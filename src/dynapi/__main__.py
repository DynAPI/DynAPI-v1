#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __version__ import __version__  # noqa
import atexit
import secrets
import os.path as p
import flask
from apiconfig import config
import dynamic_loader


app = flask.Flask(
    __name__,
    static_folder="web/static/",
    template_folder="web/",
)
app.secret_key = secrets.token_hex()
app.alive = True
atexit.register(lambda: setattr(app, 'alive', False))


ROUTES = []
PLUGINS = {}
dynamic_loader.load_folder("extra_modules")
ROUTES.extend(dynamic_loader.load_folder("routes"))
if p.isdir("plugins"):
    PLUGINS.update(dynamic_loader.load_plugins())


if __name__ == '__main__':
    # test_database_connection()
    app.run(
        host=config.get("api", "host", fallback="localhost"),
        port=config.getint("api", "port", fallback=8080),
        debug=config.getboolean("api", "debug", fallback=False),
        threaded=config.getboolean("api", "threaded", fallback=False),
        processes=config.getint("api", "processes", fallback=1)
    )
