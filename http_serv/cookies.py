class CookieAttributes(dict):
    # RFC 2109 lists these attributes as reserved:
    #   path       comment         domain
    #   max-age    secure      version
    #
    # For historical reasons, these attributes are also reserved:
    #   expires
    #
    # This is an extension from Microsoft:
    #   httponly
    #
    # This dictionary provides a mapping from the lowercase
    # variant on the left to the appropriate traditional
    # formatting on the right.
    _reserved = {
        "expires"  : "expires",
        "path"     : "Path",
        "comment"  : "Comment",
        "domain"   : "Domain",
        "max-age"  : "Max-Age",
        "secure"   : "Secure",
        "httponly" : "HttpOnly",
        "version"  : "Version",
    }
    _flags = {"secure", "httponly"}

    def __init__(self, key, value):
        self._key = key
        self.value = value
        for resv in self._reserved:
            dict.__setitem__(self, resv, "")
        self.sane_defaults()            

    def sane_defaults(self):
        dict.__setitem__(self, "httponly", True)

    def __setitem__(self, key, value):
        key = key.lower()
        if key not in self._reserved:
            raise KeyError("Invalid Attribute '%s'" %(key))
        dict.__setitem__(self, key, value)

    def export_output(self):
        resp = []
        resp.append("%s=%s" %(self._key, self.value))

        items = sorted(self.items())
        for item, value in items:
            if value == "" or item not in self._reserved:
                continue
            elif item in self._flags:
                if value:
                    resp.append(self._reserved[item])
            else: 
                resp.append("%s=%s" %(self._reserved[item], value))
        return "; ".join(resp)

    def __repr__(self):
        return str(self.value)

class Cookie(dict):
    def __init__(self, inp = None):
        if inp != None:
            self.load(inp)

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, CookieAttributes(key, value))

    def export_output(self):
        resp = []
        for i in self:
            resp.append("Set-Cookie: %s\r\n" %(self[i].export_output()))

        return "".join(resp)

    def append_attribute(self, attrib):
        dict.__setitem__(self, attrib._key, attrib)

    def load(self, inp):
        cookies = inp.split(";")
        for cookie in cookies:
            eq_split = cookie.split("=")
            self[eq_split[0]] = "=".join(eq_split[1:])

