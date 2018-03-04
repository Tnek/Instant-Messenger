#!/usr/bin/python

from httpobjects import *

def parse(tokens):
    """
        BNF is:
            Request-Line   = Method SP Request-URI SP HTTP-Version CRLF

        :param tokens: List of tokens to parse from
        :return: HTTPRequest object to fill
    """
    req = HTTPRequest(tokens[0], tokens[1], tokens[2])
    _parse_headers(req, tokens, 4)

    return req
    
def _parse_headers(req_obj, tokens, cur):
    """
        If a header is invalid, ignore it. Other HTTP servers respond an error 
        for invalid headers - may change to return malformed response on invalid
        header instead.

        :param req_obj: HTTPRequest object to fill
        :param tokens: List of tokens to parse from
        :param cur: Index of tokens where the statusline starts from
    """
    headers = []
    header_build = []
    for t in range(cur, len(tokens)):
        if tokens[t] == "\n" or tokens[t] == "\r\n":
            if _check_header(header_build):
                req_obj.headers[header_build[0]] = header_build[2:]

            header_build = []
        else:
            header_build.append(tokens[t])

def _check_header(header):
    """
        :param header: list of tokens corresponding to a header
        :return: Whether the header was valid or not
    """
    if header[1] != ':':
        return False
    return True

