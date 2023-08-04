#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import sys
import os
import os.path as p
import logging.handlers
from .fileconfig import config


log_file = config.get("logging", "file", fallback="./logs/dynapi.log")
log_file = p.abspath(log_file)
if not p.isdir(p.dirname(log_file)):
    os.makedirs(p.dirname(log_file), exist_ok=True)


handlers = [
    logging.StreamHandler(stream=sys.stdout),
    logging.handlers.RotatingFileHandler(
        filename=log_file,
        maxBytes=config.getint("logging", "max-bytes", fallback=10*1024*1024),  # ~10Mb
        backupCount=config.getint("logging", "backup-count", fallback=7),
    )
]


logging.basicConfig(
    format="{asctime} | {levelname:.3} | {name:10} | {module:15} | {funcName:20} | {lineno:3} | {message}",
    # datefmt="",
    style="{",
    level=getattr(logging, config.get("logging", "level", fallback="info").upper()),
    handlers=handlers,
)
logging.info(f"Log-File: {log_file}")
