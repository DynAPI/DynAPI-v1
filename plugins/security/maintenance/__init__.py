#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app, __version__
import textwrap
import flask
from werkzeug.exceptions import ServiceUnavailable


@app.before_request
def maintenance():
    if flask.request.path.startswith("/api"):
        raise ServiceUnavailable()
    if flask.request.path == flask.url_for("openapi"):
        return openapi_maintenance_response()


def openapi_maintenance_response():
    return dict(
        openapi="3.0.0",
        info={
            'title': "DynAPI",
            'version': __version__,
            # summary=summary,
            'description': textwrap.dedent(fr"""
            # This DynAPI instance is currently under maintenance and not available
            """),
            'x-logo': dict(
                url=flask.url_for("static", filename="assets/DynAPI.svg"),
            )
        },
    )
