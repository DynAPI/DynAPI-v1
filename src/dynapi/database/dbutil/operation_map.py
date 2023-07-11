#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from pypika import Criterion

OPMAP = {
    "==": Criterion.eq,
    "eq": Criterion.eq,
    "!=": Criterion.ne,
    "not": Criterion.ne,
    ">": Criterion.gt,
    ">=": Criterion.gte,
    "<": Criterion.lt,
    "<=": Criterion.lte,
    "glob": Criterion.glob,
    "like": Criterion.like,
}