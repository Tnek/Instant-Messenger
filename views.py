#!/usr/bin/python3
import json

from http_serv.session import *
from models import *
from app import serv, session_store, appdata

def index(req, resp):
    session = session_store.get_store(req)

    if "username" in session:
        resp.redirect("/messenger")

    elif req.method == "GET":
        resp.send_file("./static/html/index.html")

    elif req.method == "POST":
        uname = req.form["username"]

        if appdata.register(uname):
            session["username"] = req.form["username"]
            session.save(req, resp)
            resp.redirect("/messenger")
        else:
            resp.redirect("/")

def messenger(req, resp):
    session = session_store.get_store(req)
    if not "username" in session:
        resp.redirect("/")
        return
    resp.send_file("./static/html/messenger.html")

def logout(req, resp):
    session = session_store.get_store(req)
    if session:
        if "username" in session:
            appdata.disconnect(session["username"])
        session.delete()
    resp.redirect("/")

def get_users(req, resp):
    resp.headers["Content-Type"] = "application/json"
    resp.write(str(json.dumps(appdata.usernames())))

def serialize_list(items):
    return json.dumps([i.jsonify() for i in items])

def conversations(req, resp):
    session = session_store.get_store(req)

    if not "username" in session:
        resp.redirect("/")
        return

    resp.headers["Content-Type"] = "application/json"
    user = appdata.users[session["username"]]
    resp.write(serialize_list(user.conversations))


def get_msgs(req, resp):
    session = session_store.get_store(req)
    if not "username" in session:
        resp.redirect("/")
        return

    resp.headers["Content-Type"] = "application/json"
    user = appdata.users[session["username"]]
    resp.write(serialize_list(user.get_msgs()))

def msg(req, resp):
    session = session_store.get_store(req)
    if not "username" in session:
        resp.redirect("/")
        return

    if req.method == "POST":
        user = appdata.users[session["username"]]
        contents = req.form["contents"] 
        conv_id = req.form["conv"]
        conv = appdata.conversations[conv_id]

        appdata.add_msg(Message(user, contents, conv))

serv.handle("/", index, methods=["GET", "POST"])
serv.handle("/users", get_users)
serv.handle("/messenger", messenger, methods=["GET", "POST"])
serv.handle("/logout", logout)
serv.handle("/conversations", conversations)
serv.handle("/msgs", get_msgs)
