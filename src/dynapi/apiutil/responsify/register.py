#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import typing as t


converters = {}


def converter(mimes, handler=None):
    if not isinstance(mimes, (tuple, list)):
        mimes = [mimes]

    def wrapper(fn):
        for mime in mimes:
            converters[mime] = fn
        return fn

    if handler:
        return wrapper(fn=handler)
    else:
        return wrapper
