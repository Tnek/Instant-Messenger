#!/usr/bin/python3

def index(req, resp):
    if req.method == "GET":
        if "username" in req.cookies:
            resp.redirect("/messages")
        resp.send_file("./static/html/index.html")

    elif req.method == "POST":
        if "username" in req.form:
            resp.redirect("/messages")
            resp.set_cookie("username", req.form["username"])

def messages(req, resp):
    if not "username" in req.cookies:
        resp.redirect("/")
        return
    resp.send_file("./static/html/messenger.html")
