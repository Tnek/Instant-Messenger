#!/usr/bin/python3
class HTTPObject(object):
    def __init__(self, ver):
        self.version = ver
        self.headers = {}


class HTTPResponse(HTTPObject):
    def __init__(self, ver, status_code, reason_phrase):
        super().__init__(ver)


valid_methods = {"OPTIONS", "GET", "HEAD", "POST", "PUT", "DELETE", "TRACE", "CONNECT" }

class HTTPRequest(HTTPObject):
    def __init__(self, method, uri, ver):
        super().__init__(ver)
        if method not in valid_methods:
            raise ValueError("Malformed HTTP Request Method")

        self.method = method
        self.uri = uri
        self.data = ""
