#!/usr/bin/python3

import socket
import sys
import traceback

from .httpobjects import *
from .http_parse import *

# TODO: Support for
# * Session/cookies
# * Static files & url_for
# * render_template?

class HTTPServ(object):
    def __init__(self):
        self.routes = {}

    def handle(self, route, callback, methods={"GET"}):
        self.routes[route] = (callback, methods)

    def handle_connection(self, client, addr):
        tokenizer = Tokenizer()
        buf = client.recv(1024)

        while tokenizer.tokenize_buf(buf):
            buf = client.recv(1024)
        
        obj = parse(tokenizer.export_tokens())

        if "Content-Length" in obj.headers:
            obj.data = client.recv(obj.headers["Content-Length"])

        resp = self.call_handler(obj)
        client.send(resp.serialize().encode("utf-8"))

    def call_handler(self, req_obj):
        resp = HTTPResponse()
        if req_obj.uri in self.routes:
            route = self.routes[req_obj.uri]
            if req_obj.method in route[1]:
                route[0](req_obj, resp)
                return resp

        resp = HTTPResponse(data="404 Not Found", status_code=404, reason_phrase="Not Found")
        return resp

    def listen_and_serve(self, host="0.0.0.0", port=80):
        self.host = host
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

