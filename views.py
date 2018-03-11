#!/usr/bin/python3
def index(req, resp):
    if req.method == "GET":
        if "username" in req.cookies:
            resp.redirect("/messenger")
        resp.send_file("./static/html/index.html")

    elif req.method == "POST":
        if "username" in req.form:
            resp.redirect("/messenger")
            resp.cookies["username"] = req.form["username"]

def messenger(req, resp):
    if not "username" in req.cookies:
        resp.redirect("/")
        return
    resp.send_file("./static/html/messenger.html")

def logout(req, resp):
    resp.cookies["username"] = ""
    resp.cookies["username"]["expires"] = 0
    resp.redirect("/")

