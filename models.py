#!/usr/bin/python3
import time
import json

from threading import Lock

class Conversation(object):
    def __init__(self, conv_id):
        self.participants = set()
        self.conv_id = conv_id
        self.messages = []
        self.public = False
    
    def jsonify(self):
        return json.dumps({"c_id":self.conv_id,
                "usrs": [pa.uname for pa in self.participants], 
                "msgs": [msg.jsonify() for msg in self.messages]})


class Message(object):
    def __init__(self, sender, contents, conv):
        self.conv = conv
        self.sender = sender
        self.contents = contents
        self.timestamp = time.time()

    def jsonify(self):
        return json.dumps({"sender": self.sender,
                "msg": self.contents,
                "ts": self.timestamp,
                "convo": self.conv.conv_id})

class User(object):
    def __init__(self, uname):
        self.uname = uname
        self.unread_queue = []
        self.msg_lock = Lock()
        self.conversations = {}
        self.pms = {}

    def add_msg(self, msg):
        self.msg_lock.acquire()
        self.unread_queue.append(msg)
        self.msg_lock.release()

    def get_msgs(self):
        self.msg_lock.acquire()
        to_ret = self.unread_queue
        self.unread_queue = []
        self.msg_lock.release()
        return to_ret

    def __repr__(self):
        return str(self)
    def __str__(self):
        return self.uname

class Messenger(object):
    def __init__(self):
        self.users = {}
        self.public_channels = {}
        self.conversations = {}

    def register(self, uname):
        if uname not in self.users:
            self.users[uname] = User(uname)
            return True
        return False

    def usernames(self):
        return list(self.users.keys())

    def message(self, msg):
        for user in msg.conversation.participants:
            user.add_msg(msg)

    def disconnect(self, uname):
        if uname in self.users:
            del self.users[uname]
    
    def new_conversation(self, users):
        pass
