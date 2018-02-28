#!/usr/bin/python

class Token(object):
    def __init__(self, label, initial_value = ""):
        self.stack = list(initial_value)
        self.label = label
    def add(self, c):
        self.stack.append(c)
    def __repr__(self):
        return "".join(self.stack) + " " + self.label

separators = { 
    ":":"COLON",
    "\n":"LINEBREAK",
    ",":"COMMA",
    '"':"QUOTE",
    "<":"LABRACKET",
    ">":"RABRACKET",
    "?":"QUESTION",
    "=":"EQUALS",
    "{":"LBRACKET",
    "}":"RBRACKET",
    ";":"SEMICOLON",
    "@":"AT",
    "&":"AMPERSAND",
}

class Tokenizer(object):
    def __init__(self):
        self.cur_token = Token("WORD")
        self.tokens = []

    def add_char(self, c):
        if c in separators:
            self.cur_token.label = "WORD"
            self.tokens.append(self.cur_token)
            self.tokens.append(Token(separators[c], c))
            self.cur_token = Token("WORD")
        elif c == " ":
            self.cur_token.label = "WORD"
            self.tokens.append(self.cur_token)
            self.cur_token = Token("WORD")

        elif c == "\r":
            pass
        else:
            self.cur_token.add(c)

    def export_tokens(self):
        return self.tokens
    
def test():
    with open("tests/httpsample", "r") as FILE:
        a = FILE.read()
    print(a)

    t_test = Tokenizer()
    for c in a:
        t_test.add_char(c)

    for t in t_test.export_tokens():
        print("%s" %(t))

if __name__ == "__main__":
    test()
