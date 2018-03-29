import time
import json
import uuid

from threading import Lock

from event_types import *

class User(object):
    def __init__(self, uname):
        self.uname = uname
        self.unread_queue = []
        self.event_lock = Lock()

        self.conversations = set()
        self.pms = {}

    def add_event(self, msg):
        self.event_lock.acquire()
        self.unread_queue.append(msg)
        self.event_lock.release()

    def get_events(self):
        self.event_lock.acquire()
        to_ret = self.unread_queue
        self.unread_queue = []
        self.event_lock.release()
        return to_ret


class Conversation(object):
    def __init__(self, title):
        self.participants = set()
        self.messages = []
        self.public = False
        self.title = title

    def add_user(self, user):
        self.participants.add(user)
        user.conversations.add(self)

    def jsonify(self):
        return {
                "title": self.title,
                "usrs": [pa.uname for pa in self.participants], 
                "msgs": [msg.jsonify() for msg in self.messages]}

        def get_type(self):
            return "conv_create"


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

    def disconnect(self, uname):
        if uname in self.users:
            del self.users[uname]

    def new_conversation(self, title, users):
        if title in self.conversations: 
            return None
        conv = Conversation(title)

        self.conversations[title] = conv

        for u in users:
            conv.add_user(self.users[u])
            self.users[u].add_event(Event(conv))
            
        return conv

    def msg(self, msg):
        for u in msg.conv.participants:
            u.add_event(Event(msg))
