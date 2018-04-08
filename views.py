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
        resp.forbidden()
        return

    resp.headers["Content-Type"] = "application/json"
    user = appdata.users[session["username"]]
    resp.write(serialize_list(user.conversations))

def create_group(req, resp):
    session = session_store.get_store(req)
    if not "username" in session:
        resp.forbidden()
        return

    if req.method == "POST":
        user = session["username"]
        participants = req.form["users"].split("&")
        participants.append(user)
        public = req.form["is_public"] == "true"
        title = req.form["title"]
        conv = appdata.new_conversation(title, participants + [user], public)
        resp.write("OK")
    else:
        resp.forbidden()

def leave_group(req, resp):
    session = session_store.get_store(req)
    if not "username" in session:
        resp.forbidden()
        return

    if req.method == "POST":
        user = session["username"]
        conv = req.form["conv"]
        appdata.conv_leave(user, conv)
        resp.write("OK")
    else:
        resp.forbidden()
    
def fetch_events(req, resp):
    session = session_store.get_store(req)
    if not "username" in session:
        resp.forbidden()
        return

    resp.headers["Content-Type"] = "application/json"
    user = appdata.users[session["username"]]
    e = user.get_events()
    resp.write(serialize_list(e))
    
def msg(req, resp):
    session = session_store.get_store(req)
    if not "username" in session:
        resp.forbidden()
        return

    if req.method == "POST":
        if "contents" in req.form and "conv" in req.form:
            user = session["username"]
            contents = req.form["contents"] 
            conv = req.form["conv"]
            appdata.msg(user, conv, contents)
            resp.write("OK")
    else:
        resp.forbidden()

def priv_msg(req, resp):
    session = session_store.get_store(req)
    if not "username" in session:
        resp.forbidden()
        return
    if req.method == "POST":
        if "contents" in req.form and "recipient" in req.form:
            user = session["username"]
            contents = req.form["contents"]
            recipient = req.form["recipient"]
            appdata.privmsg(user, recipient, contents)
            resp.write("OK")

    else:
        resp.forbidden()

def whoami(req, resp):
    session = session_store.get_store(req)
    if "username" in session:
        resp.write(session["username"])
    else:
        resp.forbidden()

def public_conversations(req, resp):
    session = session_store.get_store(req)
    if not "username" in session:
        resp.forbidden()
        return
    
    resp.headers["Content-Type"] = "application/json"
    resp.write(serialize_list(appdata.public_conversations.values()))

def join_group(req, resp):
    session = session_store.get_store(req)
    if not "username" in session:
        resp.forbidden()
        return
    if req.method == "POST":
        user = session["username"]
        conv = req.form["conv"]

        appdata.public_conversations[conv].user_add(user)
    else:
        resp.forbidden()


serv.handle("/", index, methods=["GET", "POST"])
serv.handle("/messenger", messenger, methods=["GET", "POST"])
serv.handle("/conversations", conversations)
serv.handle("/public_conversations", public_conversations)
serv.handle("/events", fetch_events)
serv.handle("/users", get_users)
serv.handle("/logout", logout)
serv.handle("/whoami", whoami)

serv.handle("/join", join_group, methods=["POST"])
serv.handle("/newgroup", create_group, methods=["POST"])
serv.handle("/leave_group", leave_group, methods=["POST"])
serv.handle("/msg", msg, methods=["POST"])
serv.handle("/priv_msg", priv_msg, methods=["POST"])
