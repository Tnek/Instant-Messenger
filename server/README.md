#!/usr/bin/python3
from http_serv import HTTPServ, HTTPResponse

def hello(req, resp):
    resp.write("Hello world!")

def index(req, resp):
    resp.write("Hello world!")

def main():
    serv = HTTPServ()
    serv.handle("/hello", hello)
    serv.handle("/", index)
    serv.listen_and_serve(":8081")

if __name__ == "__main__":
    main()
