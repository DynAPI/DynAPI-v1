#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
__version_info__ = (0, 0, 0)
__version__ = '.'.join(str(_) for _ in __version_info__)

import os
import importlib
import flask.json.tag
from exceptions import DoNotImportException
from apiconfig import config
from util import Codes


app = flask.Flask(
    __name__,
    static_folder="web",
    template_folder="web",
)
import register_adapter  # noqa


# @app.errorhandler(Exception)
def error_handler(error: Exception):
    return dict(
        type=type(error).__name__,
        detail=str(error),
    )


@app.route("/", methods=["GET"])
def index():
    return flask.render_template(
        "home.html",
        swagger=config.getboolean("web", "swagger", fallback=False),
        redoc=config.getboolean("web", "redoc", fallback=False),
    )


ROUTES = []


for root, dirnames, files in os.walk("routes", topdown=True):
    for dirname in dirnames:
        if dirname.startswith("_"):
            dirnames.remove(dirname)
    for filename in files:
        name, ext = os.path.splitext(filename)
        if ext != ".py":
            continue
        module_name = '.'.join([*root.split(os.sep), name])
        print(f"{Codes.FG_DARK_GREY}Loading: {module_name}{Codes.RESTORE_FG}")
        try:
            module = importlib.import_module(module_name)
        except DoNotImportException:
            print(f"{Codes.FG_YELLOW}Disabled: {module_name}{Codes.RESTORE_FG}")
        # except SyntaxError:
        #     pass
        else:
            ROUTES.append(module)


if __name__ == '__main__':
    app.run(
        host=config.get("api", "host", fallback="localhost"),
        port=config.getint("api", "port", fallback=8080),
        debug=config.getboolean("api", "debug", fallback=False),
        threaded=config.getboolean("api", "threaded", fallback=False),
        processes=config.getint("api", "processes", fallback=1)
    )
