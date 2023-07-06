#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import time
import functools


def minicache(max_age: int = 60):
    def decorator(func):
        response = None
        last_refresh: int = 0

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal response, last_refresh

            if last_refresh + max_age < time.time():
                response = func(*args, **kwargs)
                last_refresh = time.time()
            return response

        return wrapper
    return decorator
