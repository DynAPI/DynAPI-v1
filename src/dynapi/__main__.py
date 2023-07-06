#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
__version_info__ = (0, 0, 0)
__version__ = '.'.join(str(_) for _ in __version_info__)

import os
import importlib
import flask
from apiconfig import config


app = flask.Flask(
    __name__,
    static_folder="web",
    template_folder="web",
)


# @app.errorhandler(Exception)
def error_handler(error: Exception):
    return dict(
        type=type(error).__name__,
        detail=str(error),
    )


@app.route("/", methods=["GET"])
def index():
    return {"Hello": "World"}


ROUTES = []


for root, dirnames, files in os.walk("routes", topdown=True):
    for dirname in dirnames:
        if dirname.startswith("_"):
            dirnames.remove(dirname)
    for filename in files:
        name, ext = os.path.splitext(filename)
        if ext != ".py":
            continue
        module = '.'.join([*root.split(os.sep), name])
        print("Loading:", module)
        ROUTES.append(
            importlib.import_module(module)
        )


if __name__ == '__main__':
    app.run(
        host=config.get("api", "host"),
        port=config.getint("api", "port"),
        debug=config.getboolean("api", "debug"),
    )
