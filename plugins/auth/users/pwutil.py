#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import os
import hmac
import hashlib


def compare_password_to_hash(pw: bytes, hsh: bytes) -> bool:
    salt, pwhashed = hsh[:32], hsh[32:]
    hashed = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=pw,
        salt=salt,
        iterations=100_000,
    )
    return hmac.compare_digest(pwhashed, hashed)
