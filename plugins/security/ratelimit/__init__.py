#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""
https://flask-limiter.readthedocs.io/en/stable/index.html
"""
from __main__ import app
import flask
import flask_limiter.util
from apiconfig import config


def get_user():
    return getattr(flask.g, 'user', "guest")


bucket_funcs = dict(
    remote_address=flask_limiter.util.get_remote_address,
    ipaddr=flask_limiter.util.get_ipaddr,
    user=get_user,
)


limiter = flask_limiter.Limiter(
    enabled=config.getboolean("plugin:ratelimit", "enabled", fallback=True),  # kill-switch
    app=app,
    key_func=bucket_funcs[config.get("plugin:ratelimit", "key_func", fallback="remote_address")],
    storage_uri="memory://",
    headers_enabled=config.getboolean("plugin:ratelimit", "headers_enabled", fallback=True),
    # default rules for all endpoints
    default_limits=config.getlist("plugin:ratelimit", "limits", fallback=None),
    # default rules per method or per endpoint
    default_limits_per_method=config.getboolean("plugin:ratelimit", "limits_per_method", fallback=True),
    # global limits for all requests
    application_limits=config.getlist("plugin:ratelimit", "application_limits", fallback=None),
)
