class Event(object):
    def __init__(self, contents):
        self.timestamp = time.time()
        self.contents = contents

    def jsonify(self):
        json.dumps({"ts":self.timestamp,
                    "type":self.contents.get_type(),
                    "contents":self.contents.jsonify()
                    })

class Message(object):
    def __init__(self, sender, conv, contents):
        super().__init__()
        self.conv = conv
        self.sender = sender
        self.contents = contents

    def jsonify(self):
        json.dumps({"sender": self.sender,
                "msg": self.contents,
                "ts": self.timestamp,
                "convo": self.conv.conv_id})

    def get_type():
        return "msg"
