#!/usr/bin/python3

import socket
socket.setdefaulttimeout(5)

import sys
import traceback
import threading

from .httpobjects import *
from .http_parse import *

# TODO: Support for
# * Session/cookies
# * Static files & url_for
# * render_template?

class ConnectionHandler(threading.Thread):
    def __init__(self, httpserv, client, addr):
        threading.Thread.__init__(self)
        self.client = client
        self.addr = addr
        self.httpserv = httpserv

    def run(self):
        try:
            persistent = True

            while persistent:
                tokenizer = Tokenizer()
                buf = self.client.recv(1024)

                while tokenizer.tokenize_buf(buf):
                    buf = self.client.recv(1024)
                
                obj = parse(tokenizer.export_tokens())

                if "Content-Length" in obj.headers:
                    obj.data = self.client.recv(obj.headers["Content-Length"])

                resp = self.httpserv.call_handler(obj)
                self.client.send(resp.serialize().encode("utf-8"))

                if resp.version == "HTTP/1.1":
                    if "Connection" in resp.headers and resp.headers["Connection"] == "close":
                        persistent = False
                else:  # older HTTP versions
                    if "Connection" in resp.headers and resp.headers["Connection"] != "keep-alive":
                        persistent = False

        except socket.timeout:
            pass
        finally:
            self.client.close()


class HTTPServ(object):
    def __init__(self):
        self.routes = {}

    def handle(self, route, callback, methods={"GET"}):
        self.routes[route] = (callback, methods)

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
                conn = ConnectionHandler(self, client, addr)
                conn.start()

        except Exception:
            traceback.print_exc()
        finally: 
            sock.close()

