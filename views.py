#!/usr/bin/python3

def index(req, resp):
    if req.method == "GET":
        resp.send_file("./static/html/index.html")

