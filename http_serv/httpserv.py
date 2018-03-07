#!/usr/bin/python3
import multiprocessing
import os
import socket
import sys

from .httpobjects import HTTPResponse, HTTPRequest
from .buffered_io import BufferedIO

class HTTPServ(object):
    def __init__(self):
        self.routes = {}
        self.static_routes = {"/static/":"./static/"}

    def handle(self, route, callback, methods=["GET"]):
        self.routes[route] = (callback, methods)

    def call_handler(self, req, resp):
        if req.uri in self.routes:
            rtable_entry = self.routes[req.uri]
            if req.method in rtable_entry[1]:
                rtable_entry[0](req, resp)
                return
            else:
                resp.status_code = 405
                resp.reason_phrase = "Method Not Allowed"
                return

        for s in self.static_routes:
            if req.uri[:len(s)]:
                real_path = os.path.abspath(self.static_routes[s] + req.uri[len(s):])

                if os.path.isfile(real_path): 
                    resp.send_file(real_path)
                    return

        resp.status_code = 404
        resp.reason_phrase = "Not Found"
        resp.write('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n' \
                '<title>404 Not Found</title>\n' \
                '<h1>Not Found</h1>\n' \
                '<p>The requested URL was not found on the server.  If you entered the URL ' \
                'manually, please check your spelling and try again.</p>')

    def _handle_req(self, sock, addr):
        persistent = True

        buf_sock = BufferedIO(sock.recv, sock.send)
        while persistent:
            req_line = buf_sock.read_until("\n").strip()
            print("[%s:%s] - %s" %(addr[0], addr[1], req_line))
            req_line = req_line.split(" ")

            ver = "HTTP/1.0"
            if len(req_line) > 2:
                ver = req_line[2]

            req = HTTPRequest(method=req_line[0], uri=req_line[1], version=ver)

            cur = buf_sock.read_until("\n")
            while cur != "\r\n" and cur != "\n":
                cur_split = cur.strip().split(": ")
                req.headers[cur_split[0]] = ": ".join(cur_split[1:])
                cur = buf_sock.read_until("\n")

            req.parse_cookies()

            if "Content-Length" in req.headers:
                req.write(buf_sock.read(int(req.headers["Content-Length"])))

            if req.method == "POST":
                req.parse_post()

            resp = HTTPResponse(status_code = 200, reason_phrase="OK")
            self.call_handler(req, resp)

            buf_sock.buf_write(resp)

            if ver == "HTTP/1.1":
                if "Connection" in req.headers and req.headers["Connection"] == "close":
                    persistent = False
            else:  # older HTTP versions
                if not "Connection" in req.headers or req.headers["Connection"] != "keep-alive":
                    persistent = False

        sock.close()

    def listen_and_serve(self, host="0.0.0.0", port=80):
        self.host = host
        self.port = int(port)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.bind((self.host, self.port))
        sock.listen(5)

        while True:
            client, addr = sock.accept()
            p = multiprocessing.Process(target=self._handle_req, args=(client,addr))
            p.start()

