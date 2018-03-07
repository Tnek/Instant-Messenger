import mimetypes

from .buffered_io import StringBuffer, FileBuffer

class HTTPObject(object):
    def __init__(self, version="HTTP/1.1"):
        """
            :param version: Version of the HTTP protocol that we're implementing
                            which defaults to HTTP/1.1 and probably should stay 
                            that. 

        """
        self.version = version
        self.headers = {}
        self.data = StringBuffer()
        self.data_len = 0

    def export_headers(self):
        if self.data_len > 0:
            self.headers["Content-Length"] = self.data_len

        return "".join("%s: %s\r\n" %(header, self.headers[header]) for header in self.headers)


class HTTPResponse(HTTPObject):
    """
        HTTP Object modeling an HTTP response.

        From rfc2616:

           After receiving and interpreting a request message, a server responds
           with an HTTP response message.

               Response      = Status-Line               ; Section 6.1
                               *(( general-header        ; Section 4.5
                                | response-header        ; Section 6.2
                                | entity-header ) CRLF)  ; Section 7.1
                               CRLF
                               [ message-body ]          ; Section 7.2

    """
    def __init__(self, status_code=200, reason_phrase="OK", version="HTTP/1.1"):
        super().__init__(version)
        self.status_code = status_code
        self.reason_phrase = reason_phrase
        self.cookies = {}
        self._main_resp = None
        self.headers["Content-Type"] = "text/html; charset=utf-8"
        #: Close by default so it's harder to write memory leaks.

    def reset_data(self):
        self.data_len = 0
        self.data = StringBuffer()

    def export_statusline(self):
        return "%s %s %s\r\n" %(self.version, self.status_code, self.reason_phrase)

    def set_cookie(self, key, value):
        # May want to do checking for invalid characters for cookies here.
        self.cookies[key] = value

    def export_cookies(self):
        if len(self.cookies) > 0:
            return "Set-Cookie: " + ";".join("%s=%s" %(cookie,
                self.cookies[cookie]) for cookie in self.cookies) + "\r\n"
        else:
            return ""

    def read(self, nbytes):
        if self._main_resp == None:
            header = self.export_statusline() + self.export_headers() + \
                     self.export_cookies() + '\r\n'
            self._main_resp = StringBuffer(header.encode('utf-8'))

        resp = self._main_resp.read(nbytes)
        if len(resp) < nbytes and self.data:
            self._main_resp = self.data
            resp += self.data.read(nbytes - len(resp))
        return resp

    def write(self, data):
        self.data_len += len(data)
        self.data.write(data)

    def close(self):
        pass

    def redirect(self, new_uri):
        self.status_code = 302
        self.reason_phrase = "Found"
        self.headers["Location"] = new_uri
        self.reset_data()
        self.write('<HTML><HEAD><meta http-equiv="content-type"' \
                    'content="text/html;charset=utf-8">\n' \
                    '<TITLE>302 Moved</TITLE></HEAD><BODY>\n' \
                    '<H1>302 Moved</H1>\n' \
                    'The document has moved\n' \
                    '<A HREF=%s">here</A>.\n' \
                    '</BODY></HTML>' %(new_uri))
        
    def send_file(self, file_dir):
        self.headers["Content-Type"] = mimetypes.guess_type(file_dir)[0]
        self.data = FileBuffer(file_dir)
        self.data_len = self.data.size()


valid_methods = {"OPTIONS", "GET", "HEAD", "POST", "PUT", "DELETE", "TRACE", "CONNECT" }

class HTTPRequest(HTTPObject):
    def __init__(self, method, uri, version):
        super().__init__(version)
        if method not in valid_methods:
            raise ValueError("Malformed HTTP Request Method")

        self.method = method
        uri_comp = uri.split("?")

        self.args = {}
        self.cookies = {}
        self.form = {}

        self.uri = uri_comp[0]

        if len(uri_comp) > 1:
            self._parse_query_str("?".join(uri_comp[1:]))


    def write(self, data):
        self.data_len += len(data)
        self.data.write(data)

    def _parse_query_str(self, data):
        args = data.split("&")
        for item in args:
            parts = item.split("=")
            self.args[parts[0]] = "=".join(parts[1:])

    def parse_post(self):
        fields = self.data.values().split("&")
        for field in fields:
            field_s = field.split("=")
            self.form[field_s[0]] = "=".join(field_s[1:])

    def parse_cookies(self):
        if "Cookie" in self.headers:
            cookies = self.headers["Cookie"].split(";")
            for cookie in cookies:
                eq_split = cookie.split("=")
                self.cookies[eq_split[0]] = "=".join(eq_split[1:])

