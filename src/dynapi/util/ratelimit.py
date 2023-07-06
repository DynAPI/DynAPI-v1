#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import http
import time
from collections import defaultdict
from _thread import start_new_thread
import functools
from flask import request, abort


def rate_limited(times: int, interval: int = 60):
    def decorator(fn):
        requests = defaultdict(int)

        @start_new_thread
        def cleaner():
            while True:
                requests.clear()
                time.sleep(interval)

        @functools.wraps
        def wrapper(*args, **kwargs):
            client = request.remote_addr
            if requests[client] >= times:
                raise abort(http.HTTPStatus.TOO_MANY_REQUESTS)
            requests[client] += 1
            return fn(*args, **kwargs)

        return wrapper
    return decorator
