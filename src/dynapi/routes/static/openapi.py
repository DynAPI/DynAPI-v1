#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app, __version__, ROUTES
import textwrap
import datetime
from collections import defaultdict
from util import minicache


@app.route("/openapi")
@minicache(max_age=30)
def openapi():
    paths = defaultdict(dict)
    for route in ROUTES:
        if not hasattr(route, 'get_openapi_spec'):
            continue
        try:
            spec = route.get_openapi_spec()
            if not isinstance(spec, dict):
                raise TypeError(f"{type(spec).__name__} is not of type dict")
        except Exception as exc:
            print(f"Failed to load openapi_spec from {route.__name__}")
            print(f"{type(exc).__name__}: {exc}")
        else:
            for path, path_spec in spec.items():
                paths[path].update(path_spec)
    return dict(
        openapi="3.0.0",
        info=dict(
            title="DynAPI",
            version=__version__,
            # summary=summary,
            description=textwrap.dedent(fr"""
            Last-Update: {datetime.datetime.now():%Y-%m-%d %H:%M}
            """.strip()),
        ),
        paths=paths,
    )
