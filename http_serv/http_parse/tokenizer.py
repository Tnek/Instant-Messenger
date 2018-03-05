#!/usr/bin/python3

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
    "\r":"CR",
    "\r\n":"CLRF",
    " ":"SPACE",
    "'":"SQUOTE",
    '"':"DQUOTE"
}

class Tokenizer(object):
    def __init__(self):
        self.cur_token = []
        self.tokens = []
        self.escape = False

    def add_char(self, c):
        if self.escape:
            if c == "'" or c == '"':
                self.cur_token.append(c)
                self.tokens.append("".join(self.cur_token))
                self.cur_token = []
                self.escape = False
            else:
                self.cur_token.append(c)

        elif c in separators:
            if len(self.cur_token) != 0:
                self.tokens.append("".join(self.cur_token))
                self.cur_token = []

            if c == "'" or c == '"':
                self.escape = True
                self.cur_token.append(c)
                return True

            if c == '\n':
                if self.tokens[-1] == '\r':
                    self.tokens.pop()
                    c = "\r\n"
                    if self.tokens[-1] == "\r\n":
                        return False

                if self.tokens[-1] == '\n':
                    return False
                else:
                    self.tokens.append(c)

            elif c != " ":
                self.tokens.append(c)
        else:
            self.cur_token.append(c)

        return True
   
    def tokenize_buf(self, buf):
        for i in buf:
            if not self.add_char(chr(i)):
                return False
        return True

    def __iter__(self):
        return map(str, self.tokens)

    def export_tokens(self):
        return list(map(str, self.tokens))

