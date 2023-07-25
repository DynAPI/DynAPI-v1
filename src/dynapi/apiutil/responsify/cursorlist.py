#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import itertools


class FakeListIterator(list):
    def __init__(self, iterable):
        self.iterable = iter(iterable)
        try:
            self.firstitem = next(self.iterable)
            self.truthy = True
        except StopIteration:
            self.truthy = False

    def __iter__(self):
        if not self.truthy:
            return iter([])
        return itertools.chain([self.firstitem], self.iterable)

    def __len__(self):
        raise NotImplementedError("Fakelist has no length")

    def __getitem__(self, i):
        raise NotImplementedError("Fakelist has no getitem")

    def __setitem__(self, i, v):
        raise NotImplementedError("Fakelist has no setitem")

    def __bool__(self):
        return self.truthy
