#!/usr/bin/python3
import string
import secrets
from .cookies import *

class Session(dict):
    """
        Class to represent key-value storage of session data and management. 
    """
    def __init__(self, store):
        self.s_id = None
        self.store = store
        self.staged_values = {}
        self.options = CookieAttributes("sessid", self.s_id)
    
    def __setitem__(self, key, val):
        self.staged_values[key] = val

    def delete(self):
        del self.store.sessions[self.s_id]

    def save(self, req, resp):
        for i in self.staged_values:
            dict.__setitem__(self, i, self.staged_values[i])
        self.staged_values = {}

        if self.s_id == None:
            self.s_id = self.store.gen_new_sessid()
            self.options.value = self.s_id
            self.store.sessions[self.s_id] = self 

        req.cookies.append_attribute(self.options)
        resp.cookies.append_attribute(self.options)

class Store(object):
    """ 
        Session storage object for getting the Session object of a specific 
        context.

        Example usage:

            session_store = Store("mysecret")

            def http_serv_route(req, resp):
                # Gets the session of a specific request
                session = session_store.get_store(req)

                # To write to the session:
                session["username"] = "alice"

                # To read from the session:
                print(session["username"])
    """
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.sessions = {}

    def gen_new_sessid(self):
        alphabet = string.ascii_letters + string.digits
        key = ''.join(secrets.choice(alphabet) for i in range(16))
        while key in self.sessions:
            key = ''.join(secrets.choice(alphabet) for i in range(16))
        return key

    def get_store(self, req):
        if "sessid" in req.cookies:
            sessid = req.cookies["sessid"]
            if sessid.value in self.sessions:
                return self.sessions[sessid.value]

        return Session(self)

