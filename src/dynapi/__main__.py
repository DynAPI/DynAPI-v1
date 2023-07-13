#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
__version_info__ = (0, 0, 0)
__version__ = '.'.join(str(_) for _ in __version_info__)

import os
import http
import hmac
import importlib
import traceback
import flask
from werkzeug.exceptions import HTTPException
from exceptions import DoNotImportException
from apiconfig import config
from database import test_database_connection
from util import TCodes
import msgpack_support


#
# app creation and configuration
#


app = flask.Flask(
    __name__,
    static_folder="web",
    template_folder="web",
)
if config.getboolean("api", "msgpack", fallback=False):
    msgpack_support.install()


# maybe better override flask.Flask.handle_http_exception
@app.errorhandler(HTTPException)
def http_error_handler(error: HTTPException):
    response = flask.jsonify(
        code=error.code,
        name=error.name,
        description=error.description,
    )
    response.status = error.code
    return response


# maybe better override flask.Flask.handle_exception
@app.errorhandler(Exception)
def server_error_handler(error: Exception):
    if isinstance(error, HTTPException):
        return error  # dunno. this part was in flask (https://flask.palletsprojects.com/en/2.3.x/errorhandling/)
    response = dict(
        type=type(error).__name__,
        detail=str(error),
    )
    if config.getboolean("api", "debug", fallback=False):
        response["traceback"] = traceback.format_tb(error.__traceback__)
    response = flask.jsonify(response)
    response.status = http.HTTPStatus.INTERNAL_SERVER_ERROR
    return response


#
# authentication system
#


CONFIGURED_USERNAME = config.get("auth", "username", fallback=None)
CONFIGURED_PASSWORD = config.get("auth", "password", fallback=None)

if CONFIGURED_USERNAME and CONFIGURED_PASSWORD:
    @app.before_request
    def verify_authorization():
        authorization = flask.request.authorization
        if not authorization:
            flask.abort(http.HTTPStatus.UNAUTHORIZED)
        correct_username = hmac.compare_digest(authorization.username, CONFIGURED_USERNAME)
        correct_password = hmac.compare_digest(authorization.password, CONFIGURED_PASSWORD)
        if not correct_username or not correct_password:
            flask.abort(http.HTTPStatus.UNAUTHORIZED)
elif CONFIGURED_USERNAME:
    print(f"{TCodes.FG_RED}Provided username without password{TCodes.RESTORE_FG}")
elif CONFIGURED_PASSWORD:
    print(f"{TCodes.FG_RED}Provided password without username{TCodes.RESTORE_FG}")


#
# dynamic import of everything in ROUTES
#


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
        # print(f"{Codes.FG_DARK_GREY}Loading: {module_name}{Codes.RESTORE_FG}")
        try:
            module = importlib.import_module(module_name)
        except DoNotImportException:
            print(f"{TCodes.FG_YELLOW}Disabled: {module_name}{TCodes.RESTORE_FG}")
        # except SyntaxError:
        #     pass
        else:
            ROUTES.append(module)


if __name__ == '__main__':
    test_database_connection()
    app.run(
        host=config.get("api", "host", fallback="localhost"),
        port=config.getint("api", "port", fallback=8080),
        debug=config.getboolean("api", "debug", fallback=False),
        threaded=config.getboolean("api", "threaded", fallback=False),
        processes=config.getint("api", "processes", fallback=1)
    )
