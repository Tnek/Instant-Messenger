import time
import json
import re

from threading import Lock

from event_types import *

class User(object):
    """ Object that represents a user. """
    def __init__(self, uname):
        self.uname = uname
        self.unread_queue = []
        self.event_lock = Lock()

        self.conv_lock = Lock()
        self.conversations = set()

        self.pms = {}
    def add_conv(self, conv):
        self.conv_lock.acquire()
        self.conversations.add(conv)
        self.conv_lock.release()

    def add_event(self, e):
        """ Adds an Event (see :class Event:`event_types.py`) to the user's message 
        queue """
        self.event_lock.acquire()
        self.unread_queue.append(e)
        self.event_lock.release()

    def get_events(self):
        self.event_lock.acquire()
        to_ret = [i for i in self.unread_queue]
        self.unread_queue = []
        self.event_lock.release()
        return to_ret

    def __repr__(self):
        return "[User %s]" %(self.uname)

class Messenger(object):
    def __init__(self):
        self.users = {}

        self.conversations_lock = Lock()
        self.conversations = {}
        self.public_conversations = {}
        self.alphanum_filter = re.compile("^[A-Za-z0-9 ]+$")

    def register(self, uname):
        if uname not in self.users and self.alphanum_filter.match(uname):
            self.users[uname] = User(uname)
            return True
        return False

    def usernames(self):
        return list(self.users.keys())

    def disconnect(self, uname):
        """ Frees the username by removing the user. """
        if uname in self.users:
            u_obj = self.users[uname]
            for conv in u_obj.conversations:
                conv.user_leave(u_obj)

            del self.users[uname]
            del u_obj

    def new_conversation(self, title, users, public=False):
        """
            Creates a new conversation object.

            :param title: Title of the conversation
            :param users: List of strings of usernames to be in the conversation
            :return: Conversation object representing new conversation if the
                     title wasn't already taken.
        """
        if title in self.conversations or not self.alphanum_filter.match(title):
            return

        conv = Conversation(title)
        self.conversations_lock.acquire()
        self.conversations[title] = conv
        if public:
            self.public_conversations[title] = conv
        self.conversations_lock.release()

        for u in users:
            if u in self.users:
                conv.silent_add_user(self.users[u])
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
            msg = PrivateMessage(sender, recipient, contents)
            msg_event = Event(msg)

            self.users[sender].add_event(msg_event)

            # Avoid double-sending when talking to yourself
            if sender != recipient:
                self.users[recipient].add_event(msg_event)
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
        if sender in self.users and conv_title in self.conversations:
            sender_obj = self.users[sender]
            conv_obj = self.conversations[conv_title]

            if sender_obj in conv_obj.participants:
                msg = Message(sender, conv_obj, contents)
                for u in conv_obj.participants:
                    u.add_event(Event(msg))
                return True

        return False

    def delete_conv(self, conv_title):
        self.conversations_lock.acquire()
        if conv_title in self.conversations:
            del self.conversations[conv_title]
        if conv_title in self.public_conversations:
            del self.public_conversations[conv_title]
        self.conversations_lock.release()

    def conv_leave(self, uname, conv_title):
        """
            Removes user from conversation. This is a wrapper around 
            :meth:`user_leave` of the Conversation object.

            :param uname: String of username of the person to leave
            :param conv_title: String of conversation title
            :return: Whether the removal was successful
        """
        if conv_title in self.conversations and uname in self.users:
            u_obj = self.users[uname]
            conv_obj = self.conversations[conv_title]

            # Free up empty conversations
            if len(conv_obj.participants) == 1:
                self.delete_conv(conv_title)

            return conv_obj.user_leave(u_obj)
        return False

