#!/usr/bin/python3
import sys

from http_serv import HTTPServ

from views import *

def main():
    app = HTTPServ()
    app.handle("/", index)

    port = 8080
    if len(sys.argv) > 1:
        port = sys.argv[1]
    app.listen_and_serve(port=port)

if __name__ == '__main__':
    main()
