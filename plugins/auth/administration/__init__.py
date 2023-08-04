#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""
username
password with constraints
admin-ping/debug-pin
"""
from __main__ import app
import hmac
import http
import base64
import flask
from pypika import PostgreSQLQuery as Query, Schema, Table
from apiconfig import config
from .util import compare_password_to_hash


USERS_SCHEMANAME = config.get('auth', 'schema') if config.has_option('auth', 'schema') else 'dynapi'
USERS_TABLENAME = config.get('auth', 'users_table') if config.has_option('auth', 'users_table') else 'users'

ADMIN_USERNAME = config.get("plugin:administration", "username")
ADMIN_PASSWORD = config.get("plugin:administration", "password")


admin = flask.Blueprint("administration", __name__,
                        static_folder='web/static/',
                        template_folder='web/',
                        url_prefix="/admin")


@admin.before_request
def verify_authentication():
    if "/static/" in flask.request.path or flask.request.path == flask.url_for("administration.login"):
        return

    authorization = flask.request.authorization
    if not (authorization and is_valid_auth(authorization.username, authorization.password))\
            and "logged-in" not in flask.session:
        if "/api/" in flask.request.path or flask.request.path == flask.url_for(".get_logs"):
            raise flask.abort(http.HTTPStatus.UNAUTHORIZED)
        else:
            return flask.redirect(flask.url_for(".login", back_to=flask.request.path))

    if not hasattr(flask.g, "user"):
        flask.g.user = "<admin>"


@admin.get("/")
def index():
    return flask.render_template("index.html")


@admin.get("/users")
def users():
    return flask.render_template("users.html")


@admin.get("/api_keys")
def api_keys():
    return flask.render_template("api_keys.html")


@admin.get("/audit-log")
def audit_log():
    return flask.render_template("audit_log.html")


def is_valid_auth(username: str, password: str):
    r"""TODO: also allow api-keys"""

    # Login over config-file
    right_username = hmac.compare_digest(username, ADMIN_USERNAME)
    right_password = hmac.compare_digest(password, ADMIN_PASSWORD)
    if right_username and right_password:
        flask.g.user = "<admin>"
        return True
    
    # Login over user with 'admin'-role
    with flask.g.db_conn as conn:
        cursor = conn.cursor()
        table = Table(USERS_TABLENAME)
        query = Query \
            .from_(Schema(USERS_SCHEMANAME).__getattr__(USERS_TABLENAME)) \
            .select('*') \
            .where(table.username == username)
        cursor.execute(str(query))
        row = cursor.fetchone()
        if not row:
            return False
        flask.g.roles = row.roles
        if not compare_password_to_hash(password.encode(), base64.b64decode(row.passwordhash.encode())):
            return False
        if "admin" in row.roles:
            flask.g.user = row.username
            return True
    return False


@admin.route("/login", methods=["GET", "POST"])
def login(back_to: str = None):
    back_to = back_to or flask.url_for(".index")
    if flask.request.method == "POST":
        username = flask.request.form.get("username")
        if username is None:
            return flask.render_template("login.html", back_to=back_to, error="Missing username in form")
        password = flask.request.form.get("password")
        if password is None:
            return flask.render_template("login.html", back_to=back_to, error="Missing password in form")
        if is_valid_auth(username=username, password=password):
            flask.session["logged-in"] = True
            flask.session["current-admin"] = username
            return flask.redirect(back_to)
        else:
            return flask.render_template("login.html", back_to=back_to, error="Invalid username or password")

    return flask.render_template("login.html", back_to=back_to)


@admin.get("/logout")
def logout():
    del flask.session["logged-in"]
    return flask.redirect(flask.url_for(".index"))


from . import crud  # noqa

app.register_blueprint(admin)
