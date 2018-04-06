import time
import json

class Event(object):
    def __init__(self, contents):
        self.timestamp = time.time()
        self.contents = contents

    def jsonify(self):
        json.dumps({"ts":self.timestamp,
                    "type":self.contents.get_type(),
                    "contents":self.contents.jsonify()
                    })
    def __repr__(self):
        return str(self.contents)

class Message(object):
    def __init__(self, sender, conv, contents):
        self.conv = conv
        self.sender = sender
        self.contents = contents

    def jsonify(self):
        return {"sender": self.sender,
                "msg": self.contents,
                "convo": self.conv.title}

    def get_type(self):
        return "msg"

    def __repr__(self):
        return "%s -> %s: %s" %(self.sender, self.conv, self.contents)

class PrivateMessage(object):
    def __init__(self, sender, recipient, contents):
        self.recipient = recipient
        self.sender = sender
        self.contents = contents

    def jsonify(self):
        return {"sender": self.sender,
                "msg": self.contents,
                "recipient": recipient}

    def get_type(self):
        return "privmsg"

    def __repr__(self):
        return "%s -> %s: %s" %(self.sender, self.recipient, self.contents)

class Conversation(object):
    def __init__(self, title):
        self.participants = set()
        self.public = False
        self.title = title

    def add_user(self, user):
        self.participants.add(user)
        user.conversations.add(self)

    def jsonify(self):
        return {
                "title": self.title,
                "usrs": [pa.uname for pa in self.participants]}

    def get_type(self):
        return "conv_create"
    def __repr__(self):
        return "Conversation %s (%s)" %(self.title, ", ".join(map(str, self.participants)))

