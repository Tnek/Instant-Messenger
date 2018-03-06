#!/usr/bin/python3

def index(req, resp):
    if req.method == "GET":
        if "user" in req.cookies:
            resp.redirect("/messages")
        resp.send_file("./static/html/index.html")

    elif req.method == "POST":
        if "asdf" in req.form:
            resp.set_cookie("user", req.form["user"])

def messages(req, resp):
    if req.method == "GET":
#        if not "user" in req.cookies:
#            resp.redirect("/")

        resp.send_file("./static/html/messenger.html")
