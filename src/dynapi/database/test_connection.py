#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import sys
from util import TCodes
from .database_connection import DatabaseConnection


def test_database_connection():
    try:
        with DatabaseConnection():
            pass
    except Exception as exc:
        print(f"{TCodes.FG_RED}Failed to connect to Database{TCodes.RESTORE_FG}")
        print(f"{type(exc).__name__}: {exc}")
        sys.exit(1)
