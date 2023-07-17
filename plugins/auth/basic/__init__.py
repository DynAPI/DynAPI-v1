#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app
import http
import hmac
import flask
from util import TCodes
from apiconfig import config


CONFIGURED_USERNAME = config.get("auth", "username", fallback=None)
CONFIGURED_PASSWORD = config.get("auth", "password", fallback=None)

if CONFIGURED_USERNAME and CONFIGURED_PASSWORD:
    @app.before_request
    def verify_authorization():
        if not flask.request.path.startswith("/api"):
            return
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
