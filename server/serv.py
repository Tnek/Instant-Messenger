#!/usr/bin/python3

from http_serv import HTTPServ, HTTPResponse

def hello(req):
    return HTTPResponse(200, "OK", data="Hello world!2")

def index(req):
    return HTTPResponse(200, "OK", data="Hello world!")

def main():
    serv = HTTPServ()
    serv.handle("/hello", hello)
    serv.handle("/", index)
    serv.listen_and_serve(":8080")

if __name__ == "__main__":
    main()
