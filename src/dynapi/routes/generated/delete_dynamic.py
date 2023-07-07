#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app
from exceptions import DoNotImportException
from apiconfig import config


if not config.getboolean("methods", "delete", fallback=False):
    raise DoNotImportException()

