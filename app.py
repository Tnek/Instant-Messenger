#!/usr/bin/python3
import sys

from http_serv import HTTPServ
from views import *

def main():
    app = HTTPServ()

    app.handle("/messenger", messenger, methods=["GET", "POST"])
    app.handle("/", index, methods=["GET", "POST"])

    port = sys.argv[1] if len(sys.argv) > 1 else 8080

    app.listen_and_serve(port=port)

if __name__ == "__main__":
    main()
