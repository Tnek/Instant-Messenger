#!/usr/bin/python
from parser import Parser

class Token(object):
    def __init__(self, label, initial_value = ""):
        self.stack = list(initial_value)
        self.label = label
    def add(self, c):
        self.stack.append(c)
    def __repr__(self):
        if self.label == "WORD":
            return "".join(self.stack) #+ " " + self.label
        else:
            return self.label

separators = { 
    ":":"COLON",
    "\n":"LF",
    ",":"COMMA",
    '"':"QUOTE",
    "<":"LABR",
    ">":"RABR",
    "?":"NANI",
    "=":"EQ",
    "{":"LBR",
    "}":"RBR",
    ";":"SEMI",
    "@":"AT",
    "&":"AMP",
    "\r":"CR",
    "\r\n":"CLRF",
}

class Tokenizer(object):
    def __init__(self):
        self.cur_token = Token("WORD")
        self.tokens = []

    def add_char(self, c):
        if c in separators:
            self.cur_token.label = "WORD"
            if len(self.cur_token.stack) != 0:
                self.tokens.append(self.cur_token)

            if c == "\n" and self.tokens[-1].label == "CR":
                self.tokens.pop()
                if self.tokens[-1].label == "CLRF":
                    return False

                c = "\r\n"

            self.tokens.append(Token(separators[c], c))
            self.cur_token = Token("WORD")
        elif c == " ":
            self.cur_token.label = "WORD"
            if len(self.cur_token.stack) != 0:
                self.tokens.append(self.cur_token)

            self.cur_token = Token("WORD")

        else:
            self.cur_token.add(c)
        return True
    
    def tokenize_buf(self, buf):
        for i in buf:
            if not self.add_char(i):
                return False
        return True

    def __iter__(self):
        return iter(self.tokens)
    
def test():
    with open("tests/httpsample", "r") as FILE:
        a = FILE.read()
    print(a)

    t_test = Tokenizer()
    for c in a:
        t_test.add_char(c)

    for t in t_test:
        print("%s" %(t))

if __name__ == "__main__":
    test()
