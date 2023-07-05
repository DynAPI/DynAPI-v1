#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app, __version__


@app.route("/openapi")
def openapi():
    # summary, description = __doc__.split('\n\n', 1)
    return dict(
        openapi="3.0.0",
        info=dict(
            title="DynAPI",
            version=__version__,
            # summary=summary,
            # description=description
            description=__doc__,
        ),
        paths={
            # "/": {}
        },
    )
