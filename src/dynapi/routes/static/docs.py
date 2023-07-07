#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""
https://stackoverflow.com/questions/6656363/proxying-to-another-web-service-with-flask
"""
from __main__ import app
import flask
from exceptions import DoNotImportException
from apiconfig import config


if not config.getboolean("web", "docs", fallback=False):
    raise DoNotImportException()


@app.route("/docs/")
def docs():
    return flask.redirect("https://dynapi-docs.readthedocs.io/en/latest/")


# @app.route("/docs/")
# @app.route("/docs/<path:path>")
# def docs(path: str = ""):
#     res = requests.request(
#         method=flask.request.method,
#         url=f"https://dynapi-docs.readthedocs.io/en/latest/{path}",
#         headers={k: v for k, v in flask.request.headers if k.lower() != 'host'},  # exclude 'host' header
#         data=flask.request.get_data(),
#         cookies=flask.request.cookies,
#         allow_redirects=False,
#     )
#
#     # NOTE we here exclude all "hop-by-hop headers" defined by RFC 2616 section 13.5.1 ref. https://www.rfc-editor.org/rfc/rfc2616#section-13.5.1
#     # region exlcude some keys in :res response
#     excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
#     headers = [
#         (k, v) for k, v in res.raw.headers.items()
#         if k.lower() not in excluded_headers
#     ]
#     # endregion exlcude some keys in :res response
#
#     return flask.Response(res.content, res.status_code, headers)
