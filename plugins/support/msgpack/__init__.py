#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import msgpack
from apiconfig import config
from apiutil.responsify import register
from apiutil.responsify.convert2default import convert2default


def msgpack_dumps(data):
    return msgpack.dumps(data, default=convert2default), "application/msgpack"


if config.getboolean("api", "msgpack", fallback=False):
    register.converter("application/msgpack", msgpack_dumps)
