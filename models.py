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

    def __repr__(self):
        return "[User %s]" %(self.uname)

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
        """
            Creates a new conversation object.

            :param title: Title of the conversation
            :param users: List of strings of usernames to be in the conversation
            :return: Conversation object representing new conversation if the
                     title wasn't already taken.
        """
        if title in self.conversations:
            return

        conv = Conversation(title)
        self.conversations[title] = conv

        for u in users:
            conv.add_user(self.users[u])
            self.users[u].add_event(Event(conv))
            
        return conv

    def privmsg(self, sender, recipient, contents):
        """ 
            Sends a private message to another user.

            :param sender: String of username of the sender
            :param recipient: String of username of the recipient
            :param contents: Content of the message
            :return: Whether the message was successfuly sent
        """
        if sender in self.users and recipient in self.users:
            sender = self.users[sender]
            recipient = self.users[recipient]
            msg = PrivateMessage(sender, recipient, contents)
            recipient.add_event(Event(msg))
            return True

        return False

    def msg(self, sender, conv_title, contents):
        """ 
            Sends a message to the conversation

            :param sender: String of username of the sender
            :param conv_title: String of conversation title
            :param contents: Contents of the message
            :return: Whether the message was successfully sent
        """
        print("msg [%s] [%s]" %(sender, conv_title))
        if sender in self.users and conv_title in self.conversations:
            print(self.conversations)
            sender_obj = self.users[sender]
            conv_obj = self.conversations[conv_title]

            if sender_obj in conv_obj.participants:
                print("sender obj not in participants")
                msg = Message(sender, conv_obj, contents)
                for u in conv_obj.participants:
                    u.add_event(Event(msg))
                return True

        return False

