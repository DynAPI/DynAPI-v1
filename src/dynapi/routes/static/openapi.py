#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
from __main__ import app, __version__, ROUTES, PLUGINS
import textwrap
import datetime
import traceback
import itertools
from collections import defaultdict
from database import dbutil
from exceptions import DoNotImportException
from apiconfig import config


if not config.getboolean("web", "redoc", fallback=False) and not config.getboolean("web", "swagger", fallback=False):
    raise DoNotImportException()


@app.get("/openapi")
# @minicache(max_age=30)
def openapi():
    try:
        paths = defaultdict(dict)
        tables_meta = dbutil.list_tables_meta()
        for route in itertools.chain(ROUTES, PLUGINS.values()):
            if not hasattr(route, 'get_openapi_spec'):
                continue
            try:
                spec = route.get_openapi_spec(tables_meta)
                if not isinstance(spec, dict):
                    raise TypeError(f"{type(spec).__name__} is not of type dict")
            except Exception as exc:
                print(f"Failed to load openapi_spec from {route.__name__}")
                traceback.print_exception(type(exc), exc, exc.__traceback__)
            else:
                for path, path_spec in spec.items():
                    paths[path].update(path_spec)
        return dict(
            openapi="3.0.0",
            info={
                'title': "DynAPI",
                'version': __version__,
                # summary=summary,
                'description': textwrap.dedent(fr"""
                Last-Update: {datetime.datetime.now():%Y-%m-%d %H:%M}
                """),
                'x-logo': dict(
                    url="/static/assets/DynAPI.svg",
                )
            },
            tags=[
                dict(
                    name="Stats",
                    description="Status Information",
                ),
                dict(
                    name="Meta",
                    description="Meta Information",
                ),
            ],
            externalDocs=dict(
                url="https://dynapi-docs.readthedocs.io/en/latest/",
                description="Read the DynAPI-Docs"
            ),
            paths=paths,
        )
    except Exception as exc:
        return openapi_error_fallback(exception=exc)


def openapi_error_fallback(exception: Exception):
    return dict(
        openapi="3.0.0",
        info={
            'title': "DynAPI",
            'version': __version__,
            # summary=summary,
            'description': textwrap.dedent(fr"""
            Last-Update: {datetime.datetime.now():%Y-%m-%d %H:%M}
            
            # Failed to load openapi-specification
            **Type:** {type(exception).__name__}  
            **Detail:** {exception}
            """),
            'x-logo': dict(
                url="/static/assets/DynAPI.svg",
            )
        },
    )
