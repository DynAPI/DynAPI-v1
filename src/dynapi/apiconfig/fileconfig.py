#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import __file__ as main_file
import configparser
from pathlib import Path
import os
import os.path as p


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
for location in [
    os.getenv("DYNAPI_CONF") or "",
    Path(main_file).parent / "api.conf",
    Path().cwd() / "api.conf",
    Path.home() / ".dynapi.conf",
    Path("/") / "etc" / "dynapi" / "api.conf",
]:
    if p.isfile(location):
        if config.read([location]):
            break
else:
    raise FileNotFoundError("api.conf")
