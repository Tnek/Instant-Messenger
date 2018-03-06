#!/usr/bin/python

from ..httpobjects import *
from .tokenizer import Tokenizer

def parse(tokens):
    """
        BNF is:
            Request-Line   = Method SP Request-URI SP HTTP-Version CRLF

        :param tokens: List of tokens to parse from
        :return: HTTPRequest object to fill
    """
    if tokens[2] == '\n':
        req = HTTPRequest(tokens[0], tokens[1], "HTTP/1.0")
    else:
        req = HTTPRequest(tokens[0], tokens[1], tokens[2])
    _parse_headers(req, tokens, 4)
    if "Cookie" in req.headers:
        _parse_cookies(req, req.headers["Cookie"])

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

def _parse_cookies(req_obj, cookie_tokens):
    """
        Parses cookies

        BNF (rfc6265) is:
           OWS            = *( [ obs-fold ] WSP )
                            ; "optional" whitespace
           obs-fold       = CRLF

           cookie-header = "Cookie:" OWS cookie-string OWS
           cookie-string = cookie-pair *( ";" SP cookie-pair )

        :param req_obj: HTTPRequest object to fill cookies
        :param tokens: List of cookie tokens to parse from
    """
    builder = []
    cookie_token_built = []

    for t in cookie_tokens: 
        if t == ";":
            cookie_token_built.append(builder)
            builder = []
        else:
            builder.append(t)

    if len(builder) > 0:
        cookie_token_built.append(builder)

    for cookie_t in cookie_token_built:
        lval = []
        for t in range(len(cookie_t)):
            if cookie_t[t] == "=":
                req_obj.cookies["".join(cookie_t[:t])] = "".join(cookie_t[t+1:])
                continue

def parse_post(req_obj):
    fields = req_obj.data.split("&")
    for field in fields:
        field_s = field.split("=")
        req_obj.form[field_s[0]] = "=".join(field_s[1:])

