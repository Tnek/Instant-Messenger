#!/usr/bin/python3

def index(req, resp):
    resp.data = "./static/html/index.html"
    resp.is_static = True

