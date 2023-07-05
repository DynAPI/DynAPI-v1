#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
__version_info__ = (0, 0, 0)
__version__ = '.'.join(str(_) for _ in __version_info__)

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


import routes.static.redoc
import routes.static.swagger
import routes.static.openapi

import routes.meta.list_tables_meta
import routes.meta.list_tables
import routes.meta.list_columns

import routes.generated.select_dynamic


if __name__ == '__main__':
    app.run(
        host=config.get("api", "host"),
        port=config.getint("api", "port"),
        debug=config.getboolean("api", "debug"),
    )
