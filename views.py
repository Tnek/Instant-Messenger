#!/usr/bin/python3
from http_serv.session import *
store = Store("janky key")

def index(req, resp):
    session = store.get_store(req)

    if "username" in session:
        resp.redirect("/messenger")

    elif req.method == "GET":
        resp.send_file("./static/html/index.html")

    elif req.method == "POST":
        session["username"] = req.form["username"]
        session.save(req, resp)
        resp.redirect("/messenger")


def messenger(req, resp):
    session = store.get_store(req)
    if not "username" in session:
        resp.redirect("/")
        return
    resp.send_file("./static/html/messenger.html")

def logout(req, resp):
    session = store.get_store(req)
    session.delete()
    resp.redirect("/")

def users(req, resp):
    pass

