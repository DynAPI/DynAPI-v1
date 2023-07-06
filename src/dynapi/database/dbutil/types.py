#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from dataclasses import dataclass


@dataclass(frozen=True)
class TableMeta:
    schema: str
    table: str
    owner: str


@dataclass(frozen=True)
class TableColumn:
    name: str
    data_type: str
    # is_nullable: str
    # is_identity: str
    # is_generated: str
    # is_updatable: str
