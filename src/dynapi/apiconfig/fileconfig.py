#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import configparser


config = configparser.ConfigParser(
    allow_no_value=False,
    delimiters=("=", ":"),
    comment_prefixes=("#", ";"),
    inline_comment_prefixes="#",
    strict=True,
    empty_lines_in_values=False,
    interpolation=configparser.ExtendedInterpolation(),
)
config.optionxform = lambda option: option.lower().replace('-', '_')  # 'Hello-World' => 'hello_world'
if not config.read(["api.conf"]):
    raise FileNotFoundError("api.conf")
