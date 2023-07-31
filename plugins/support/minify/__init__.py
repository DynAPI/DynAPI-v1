#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app
import flask_minify
from apiconfig import config


passive = config.getboolean("plugin:minify", "passive", fallback=False)


minify = flask_minify.Minify(
    app=None if passive else app,
    html=config.getboolean("plugin:minify", "html", fallback=True),
    js=config.getboolean("plugin:minify", "js", fallback=True),
    cssless=config.getboolean("plugin:minify", "css", fallback=None),
    fail_safe=config.getboolean("plugin:minify", "fail_safe", fallback=True),
    bypass=config.getlist("plugin:minify", "bypass", fallback=""),
    bypass_caching=config.getlist("plugin:minify", "bypass_caching", fallback=""),
    caching_limit=0,  # we don't want caching
    # caching_limit=config.getboolean("plugin:minify", "caching_limit", fallback=0),  # recommended to not touch this
    static=config.getboolean("plugin:minify", "fail_safe", fallback=True),
    passive=passive,
)
