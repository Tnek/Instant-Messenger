import mimetypes

from .buffered_io import StringBuffer, FileBuffer
from .cookies import Cookie
from .utils import urldecode

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
        self.cookies = Cookie()

    def export_headers(self):
        if self.data_len > 0:
            self.headers["Content-Length"] = self.data_len

        return "".join("%s: %s\r\n" %(header, self.headers[header]) for header in sorted(self.headers))


class HTTPResponse(HTTPObject):
    """
        HTTP Object modeling an HTTP response.  

        This HTTPResponse object implements the BufferedIO interface defined in 
        :file:`buffered_io.py` so that transmission of larger responses can be 
        buffered.

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
        self._main_resp = None
        self.headers["Content-Type"] = "text/html; charset=utf-8"

    def reset_data(self):
        """ 
            Empty data field of the response. Call this method instead of 
            setting .data to empty so that length and :method:`write` still work
            correctly.
        """
        self.data_len = 0
        self.data = StringBuffer()

    def export_statusline(self):
        return "%s %s %s\r\n" %(self.version, self.status_code, self.reason_phrase)

    def read(self, nbytes):
        """
            Implementation of :method:`read` from the BufferedIO interface 
            defined in buffered_io.py. This allows for a buffered write of the 
            HTTP response which the server should respond with.
        """
        if self._main_resp == None:
            header = self.export_statusline() + self.export_headers() + \
                     self.cookies.export_output() + '\r\n'
            self._main_resp = StringBuffer(header.encode('utf-8'))

        resp = self._main_resp.read(nbytes)
        if len(resp) < nbytes and self.data:
            self._main_resp = self.data
            resp += self.data.read(nbytes - len(resp))
        return resp

    def write(self, data):
        """ Append data to the response.  """
        self.data_len += len(data)
        self.data.write(data)

    def close(self):
        """ 
            Implementation of :method:`close` from the BufferedIO interface 
            defined in buffered_io.py.
        """
        pass

    def redirect(self, new_uri):
        """
            Turn object into a redirect

            :param new_uri: New location
        """
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
        """
            Does a buffered transmission of a larger file.

            :param file_dir: Directory of the file to respond with
        """
        self.headers["Content-Type"] = mimetypes.guess_type(file_dir)[0]
        self.data = FileBuffer(file_dir)
        self.data_len = self.data.size()

    def forbidden(self):
        """ Turn object into a 403 Forbidden """
        self.status_code = 403
        self.reason_phrase = "Forbidden"
        self.reset_data()
        self.write('<html><head><title>403 Forbidden</title></head> <body bgcolor'
                    '="white"> <center><h1>404 Not Found</h1></center></body></html>')


valid_methods = {"OPTIONS", "GET", "HEAD", "POST", "PUT", "DELETE", "TRACE", "CONNECT" }

class HTTPRequest(HTTPObject):
    def __init__(self, method, uri, version):
        super().__init__(version)
        if method not in valid_methods:
            raise ValueError("Malformed HTTP Request Method")

        self.method = method
        uri_comp = uri.split("?")

        self.args = {}
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
            parts = list(map(urldecode, item.split("=")))
            self.args[parts[0]] = "=".join(parts[1:])

    def parse_post(self):
        fields = self.data.values().split("&")
        for field in fields:
            field_s = list(map(urldecode, field.split("=")))
            self.form[field_s[0]] = "=".join(field_s[1:])
