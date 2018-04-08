import time
import json
from threading import Lock

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
        self.timestamp = time.strftime("%m/%d/%y - %I:%M %p", time.gmtime())
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
            :param sender: String of sender's username
            :param conv: Conversation object representing the conversation
            :param contents: String with the contents of the message
        """
        self.conv = conv
        self.sender = sender
        self.contents = contents

    def jsonify(self):
        return {"sender": self.sender,
                "contents": self.contents,
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
                "contents": self.contents,
                "recipient": self.recipient}

    def get_type(self):
        return "privmsg"

    def __repr__(self):
        return "%s -> %s: %s" %(self.sender, self.recipient, self.contents)

class ConversationMessage(object):
    """ Represents system events for user's actions inside a conversation """
    def __init__(self, sender, convo):
        self.convo = convo
        self.sender = sender

    def jsonify(self):
        return {"sender": self.sender,
                "convo": self.convo}

class ConversationLeave(ConversationMessage):
    def get_type(self):
        return "conv_leave"

class ConversationJoin(object):
    def get_type(self):
        return "conv_join"

class Conversation(object):
    def __init__(self, title):
        self.participants_lock = Lock()
        self.participants = set()
        self.public = False
        self.title = title

    def add_user(self, user):
        self.participants_lock.acquire()
        self.participants.add(user)
        user.conversations.add(self)
        self.participants_lock.release()

    def jsonify(self):
        return {"title": self.title,
                "usrs": [pa.uname for pa in self.participants]}

    def get_type(self):
        return "conv_create"

    def user_add(self, user):
        for user in self.participants:
            user.add_event(Event(ConversationJoin(user.uname, self.title)))
        self.participants.add(user)
        user.add_event(Event(self))

    def user_leave(self, user):
        self.participants_lock.acquire()
        if user in self.participants:
            self.participants.remove(user)
            conv_leave = ConversationLeave(user.uname, self.title)

            for u in self.participants:
                u.add_event(Event(conv_leave))
            self.participants_lock.release()
            return True

        self.participants_lock.release()
        return False

    def __repr__(self):
        return "Conversation %s (%s)" %(self.title, ", ".join(map(str, self.participants)))

