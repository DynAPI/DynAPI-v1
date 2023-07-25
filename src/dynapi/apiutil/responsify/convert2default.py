#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import uuid
import decimal
import dataclasses
from datetime import date, datetime
from werkzeug.http import http_date


def convert2default(obj):
    # this function is similar/identical to flask.json.JsonEncoder.default(self, obj)
    if isinstance(obj, (date, datetime)):
        return http_date(obj)
    if isinstance(obj, (decimal.Decimal, uuid.UUID)):
        return str(obj)
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    if hasattr(obj, "__html__"):
        return str(obj.__html__())
    if hasattr(obj, "asdict"):  # dunno but could be helpful
        return obj.asdict()
    if hasattr(obj, "_asdict"):  # namedtuple
        return obj._asdict()  # noqa
    return vars(obj)  # failsafe? should this be kept in
    # raise TypeError(f"Object of type '{type(obj).__name__}' is not serializable")
