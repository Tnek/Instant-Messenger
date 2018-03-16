#!/usr/bin/python3
import time
class Conversation(object):
    def __init__(self, conv_id):
        self.participants = set()
        self.conv_id = conv_id

class Message(object):
    def __init__(self, sender, contents):
        self.sender = sender
        self.contents = contents
        self.timestamp = time.time()

class User(object):
    def __init__(self, uname):
        self.uname = uname
        self.pms = set()

    def __repr__(self):
        return str(self)
    def __str__(self):
        return self.uname

class Messenger(object):
    def __init__(self):
        self.users = {}
        self.conversations = {}

    def register(self, uname):
        if uname not in self.users:
            self.users[uname] = User(uname)
            return True
        return False

    def usernames(self):
        return list(self.users.keys())

    def message(self, msg, recipient):
        pass

