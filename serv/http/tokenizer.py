#!/usr/bin/python
from parser import Parser

class Token(object):
    def __init__(self, initial_value = ""):
        self.stack = list(initial_value)
    def add(self, c):
        self.stack.append(c)
    def __repr__(self):
        return "".join(self.stack) 

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
    " ":"SPACE",
    "'":"SQUOTE",
    '"':"DQUOTE"
}

class Tokenizer(object):
    def __init__(self):
        self.cur_token = Token()
        self.tokens = []
        self.escape = False

    def add_char(self, c):
        if self.escape:
            if c == "'" or c == '"':
                self.tokens.append(self.cur_token)
                self.tokens.append(c)
                self.escape = False
            else:
                self.cur_token.stack.append(c)

        elif c in separators:
            if len(self.cur_token.stack) != 0:
                self.tokens.append(self.cur_token)
                self.cur_token = Token()

            if c == "'" or c == '"':
                self.escape = True

            if c == '\n':
                if self.tokens[-1] == '\r':
                    self.tokens.pop()
                    c = "\r\n"

                if self.tokens[-1] == "\r\n" or self.tokens[-1] == '\n':
                    return False
                else:
                    self.tokens.append(c)

            elif c != " ":
                self.tokens.append(c)
        else:
            self.cur_token.add(c)

        return True

   
    def tokenize_buf(self, buf):
        for i in buf:
            if not self.add_char(i):
                return False
        return True

    def __iter__(self):
        return map(str, self.tokens)

    def export_tokens(self):
        return map(str, self.tokens)

def test():
    with open("tests/httpsample2", "r") as FILE:
        a = FILE.read()
    print(a)

    t_test = Tokenizer()
    for c in a:
        if not t_test.add_char(c):
            break

    print(t_test.export_tokens())

if __name__ == "__main__":
    test()
