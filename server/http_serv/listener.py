#!/usr/bin/python3

import socket
import sys
import traceback

from tokenizer import Tokenizer
from httpobjects import *
import parser

class HTTPServ(object):
    def __init__(self):
        self.routes = {}

    def add_handler(self, route, callback, methods={"GET"}):
        self.routes[route] = (callback, methods)

    def handle_connection(self, client, addr):
        tokenizer = Tokenizer()
        buf = client.recv(1024)

        while tokenizer.tokenize_buf(buf):
            buf = client.recv(1024)
        
        obj = parser.parse(tokenizer.export_tokens())

        if "Content-Length" in obj.headers:
            obj.data = client.recv(obj.headers["Content-Length"])

        resp = self.call_handler(obj)
        client.send(resp.serialize().encode("utf-8"))

    def call_handler(self, req_obj):
        if req_obj.uri in self.routes:
            route = self.routes[req_obj.uri]
            if req_obj.method in route[1]:
                return route[0](req_obj)

        return HTTPResponse(404, "Not Found", data="Not found")

    def listen_and_serve(self, serv_addr):
        host, port = serv_addr.split(":")
        if host == "":
            self.host = "0.0.0.0"
        if port == "http":
            port = 80
        self.port = int(port)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind((self.host, self.port))
            sock.listen(5)

            while True:
                client, addr = sock.accept()
                self.handle_connection(client, addr)

        except Exception:
            traceback.print_exc()
        finally: 
            sock.close()


def test():
    serv = HTTPServ()
    serv.listen_and_serve(":" + sys.argv[1])

if __name__ == "__main__":
    test()
