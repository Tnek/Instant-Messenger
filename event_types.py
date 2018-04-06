import time
import json

class Event(object):
    """ 
        Generic wrapper for events. This encapsulates all other types of events.

        To define your own event, include the following methods:

        def jsonify() - 
            :return: a dictionary of relevant key-vaue pairs to be transmitted for 
            the event

        def get_type() - 
            This method may not be necessary if we use the name of the parent 
            class instead such as with type(self).__name__. 

            :return: a string that signifies the type of event. 

    """
    def __init__(self, contents):
        self.timestamp = time.time()
        self.contents = contents

    def jsonify(self):
        return {"ts":self.timestamp,
                "type":self.contents.get_type(),
                "event_obj":self.contents.jsonify()
                }

    def __repr__(self):
        return str(self.jsonify())

class Message(object):
    def __init__(self, sender, conv, contents):
        """
            :param sender: User object representing the sender
            :param conv: Conversation object representing the conversation
            :param contents: String with the contents of the message
        """
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

