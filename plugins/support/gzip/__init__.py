#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""
This plugin is a rewritten version of https://github.com/shengulong/flask-compress/blob/master/flask_compress.py
"""
from __main__ import app
import gzip
import flask
from werkzeug import datastructures
from apiconfig import config


if config.has_option("api", "gzip-on"):
    gzip_on = [mimetype.strip() for mimetype in config.get("api", "gzip-on", fallback=None).split(",")]
else:
    gzip_on = ["text/html", "text/css", "application/javascript", "text/xml", "application/json"]
gzip_on = datastructures.MIMEAccept((mime, 1) for mime in gzip_on)

gzip_after = config.getint("api", "gzip-after", fallback=500)


def gzip_compression(response: flask.Response) -> flask.Response:
    if (
        not (200 <= response.status_code < 300) or  # bad response-code
        'gzip' not in flask.request.accept_encodings or  # gzip not allowed from client
        response.content_length is not None and response.content_length < gzip_after or  # content too small
        'Content-Encoding' in response.headers or  # already encoded
        response.mimetype not in gzip_on  # invalid mimetype
    ):
        return response

    response.direct_passthrough = False

    response.data = gzip.compress(response.data)

    response.headers['Content-Encoding'] = 'gzip'

    vary = response.headers.get('Vary')
    if not vary:
        response.headers['Vary'] = 'Accept-Encoding'
    elif 'accept-encoding' not in vary.lower():
        response.headers['Vary'] = '{}, Accept-Encoding'.format(vary)

    return response


if config.getboolean("api", "gzip", fallback=False):
    app.after_request(gzip_compression)
