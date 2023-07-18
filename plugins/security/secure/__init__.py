#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app
import http
import flask


@app.before_request
def check_if_secure():
    if not flask.request.is_secure:
        raise flask.abort(
            http.HTTPStatus.BAD_REQUEST,
            description=f"no secure protocol was used ({flask.request.scheme} instead of https or wss)"
        )
