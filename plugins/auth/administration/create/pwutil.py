#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import os
import hashlib


def generate_password_hash(pw: bytes) -> bytes:
    salt = os.urandom(32)
    hashed = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=pw,
        salt=salt,
        iterations=100_000,
    )
    return salt + hashed
