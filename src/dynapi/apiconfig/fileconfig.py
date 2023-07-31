#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import __file__ as main_file, __version__ as main_version
import os
import sys
import re
import configparser
from pathlib import Path


if "-h" in sys.argv or "--help" in sys.argv:
    print(r"""
usage: dynapi [-h] [-v] [config-file]

positional arguments:
    config-file         check for updates and install them

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
    """.strip())
    sys.exit(0)
if "-v" in sys.argv or "--version" in sys.argv:
    print(main_version)
    sys.exit(0)
argument_config_file = sys.argv[1] if len(sys.argv) > 1 else None


class ExtendedMethodsParser(configparser.ConfigParser):
    @staticmethod
    def _str2list(string: str):
        return [val for val in re.split(r"\s*[,;]\s*", string) if val]

    def getlist(self, section, option, *, raw=False, vars=None, fallback=getattr(configparser, '_UNSET')):
        return self._get_conv(section, option, self._str2list, raw=raw, vars=vars, fallback=fallback)


config = ExtendedMethodsParser(
    allow_no_value=False,
    delimiters=("=", ":"),
    comment_prefixes=("#", ";"),
    inline_comment_prefixes="#",
    strict=True,
    empty_lines_in_values=False,
    interpolation=configparser.ExtendedInterpolation(),
)
config.optionxform = lambda option: option.lower().replace('-', '_')  # 'Hello-World' => 'hello_world'
config.read_string(r"""
[methods:dynapi]
get=False
post=False
delete=False
put=False
patch=False
""")
for location in [
    Path(argument_config_file or ""),
    Path(os.getenv("DYNAPI_CONF") or ""),
    Path(main_file).parent / "api.conf",
    Path().cwd() / "api.conf",
    Path.home() / ".dynapi.conf",
    Path("/") / "etc" / "dynapi" / "api.conf",
]:
    location = location.absolute()
    if location.is_file():
        if config.read([location]):
            print(f"Conf-File: {location}")
            break
else:
    raise FileNotFoundError("api.conf")
