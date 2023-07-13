#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from dataclasses import dataclass


@dataclass(frozen=True)
class TableMeta:
    schema: str
    table: str
    type: str


@dataclass(frozen=True)
class TableColumn:
    name: str
    data_type: str
    # is_nullable: str
    # is_identity: str
    # is_generated: str
    # is_updatable: str


@dataclass(frozen=True)
class Count:
    count: int


@dataclass(frozen=True)
class Constraints:
    constraint_name: str
    constraint_type: str
    referenced_table_name: str
    referenced_column_name: str
    data_type: str
    is_updatable: str

