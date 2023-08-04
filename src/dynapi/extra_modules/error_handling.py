#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app
import http
import traceback
import flask
from werkzeug.exceptions import HTTPException
from apiconfig import config


# maybe better override flask.Flask.handle_http_exception
@app.errorhandler(HTTPException)
def http_error_handler(error: HTTPException):
    flask.g.exception_name = type(error).__name__
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
    flask.g.exception_name = type(error).__name__
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
