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

            resp.cookies["username"]["secure"] = True

def messenger(req, resp):
    if not "username" in req.cookies:
        resp.redirect("/")
        return
    resp.send_file("./static/html/messenger.html")
