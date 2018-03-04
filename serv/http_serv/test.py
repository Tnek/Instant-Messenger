#!/usr/bin/python3

from parser import *
from tokenizer import *

def test():
    with open("tests/httpsample2", "r") as FILE:
        a = FILE.read()
    print(a)

    t_test = Tokenizer()
    for c in a:
        if not t_test.add_char(c):
            break
    #print(t_test.export_tokens())
    httpobj = parse(t_test.export_tokens())
    print(httpobj.headers)

    for i in httpobj.headers:
        print("%s -> %s" %(i, httpobj.headers[i]))

if __name__ == "__main__":
    test()
