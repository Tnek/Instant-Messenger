#!/usr/bin/python3

import datetime
import os
import os.path
import socket
import mimetypes
import sys
import traceback
import threading
import traceback

from .httpobjects import *
from .http_parse import *

socket.setdefaulttimeout(5)

# TODO: Support for
# * Sessioning
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
                print(tokenizer.export_tokens())
                print(obj.cookies)

                if "Content-Length" in obj.headers:
                    obj.data = self.client.recv(int(obj.headers["Content-Length"][0]))

                resp = self.httpserv.call_handler(obj)

                if resp == None:
                    resp = self.httpserv.serve_static(obj)

                if resp == None:
                    resp = HTTPResponse(data='<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n'
                            '<title>404 Not Found</title>\n'
                            '<h1>Not Found</h1>\n'
                            '<p>The requested URL was not found on the server.  If you entered the URL '
                            'manually, please check your spelling and try again.</p>', 
                            status_code=404, reason_phrase="Not Found")

                print(resp.serialize())

                self.client.send(resp.serialize().encode("utf-8"))

                if resp.is_static:
                    length = os.path.getsize(resp.data)
                    with open(resp.data, "r") as FILE:
                        d = FILE.read(1024)
                        while d:
                            print(d)
                            self.client.send(d.encode("utf-8"))
                            d = FILE.read(1024)

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

def epoch_to_httpdate(self, epoch):
    pass

def httpdate_to_epoch(self, httpdate):
    pass

def _check_conditions(req_obj, real_path):
    last_modified = os.path.getmtime(real_path)

    return True

class HTTPServ(object):
    def __init__(self):
        self.static_routes = {"/static/":"./static/"}
        self.routes = {}
    
    def serve_static(self, req_obj):
        """
            Current algorithm for determining static routes is kind of janky. 
            There is probably a better way of doing this. This also fails with 
            relative pathing for resources.

            Directory traversal by default is not supported.

            :param req_obj: Initial request object
            :return: HTTP 200 if needs to send file, HTTP 304 if passes GET 
                     conditions, None if no such route for the file
        """
        resp = None
        for s in self.static_routes:
            if s == req_obj.uri[:len(s)]:
                real_path = os.path.abspath(self.static_routes[s] + req_obj.uri[len(s):])

                if os.path.isfile(real_path): 
                    if _check_conditions(req_obj, real_path):
                        resp = HTTPResponse(status_code=200, reason_phrase="OK", data=real_path)
                        resp.is_static = True
                        resp.headers["Content-Type"] = mimetypes.guess_type(real_path)[0]
                    else:
                        resp = HTTPResponse(status_code=304, reason_phrase="Not Modified")

        return resp
 
    def handle(self, route, callback, methods={"GET"}):
        self.routes[route] = (callback, methods)

    def call_handler(self, req_obj):
        resp = HTTPResponse()
        if req_obj.uri in self.routes:
            route = self.routes[req_obj.uri]
            if req_obj.method in route[1]:
                route[0](req_obj, resp)
                return resp
        
        return None


    def listen_and_serve(self, host="0.0.0.0", port=80):
        self.host = host
        self.port = int(port)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind((self.host, self.port))
            sock.listen(5)

            while True:
                try:
                    client, addr = sock.accept()
                    conn = ConnectionHandler(self, client, addr)
                    conn.start()
                except socket.timeout:
                    pass

        except Exception:
            traceback.print_exc()
        finally: 
            sock.close()

