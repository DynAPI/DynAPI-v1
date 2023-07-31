#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""
username
password with constraints
admin-ping/debug-pin
"""
from __main__ import app
import http
import hmac
import flask


admin = flask.Blueprint("administration", __name__,
                        static_folder='web/static/',
                        template_folder='web/',
                        url_prefix="/admin")


@admin.before_request
def verify_authentication():
    if "/static/" in flask.request.path or flask.request.path == flask.url_for("administration.login"):
        return
    if not flask.session.get("logged-in"):
        return flask.redirect(flask.url_for(".login", back_to=flask.request.path))
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


@admin.route("/login", methods=["GET", "POST"])
def login(back_to: str = None):
    back_to = back_to or flask.url_for(".index")
    if flask.request.method == "POST":
        uname = flask.request.form.get("username")
        if uname is None:
            return flask.render_template("login.html", back_to=back_to, error="Missing username in form")
        pword = flask.request.form.get("password")
        if pword is None:
            return flask.render_template("login.html", back_to=back_to, error="Missing password in form")
        right_username = hmac.compare_digest(uname, "admin")
        right_password = hmac.compare_digest(pword, "admin")
        if right_username and right_password:
            flask.session["logged-in"] = True
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
