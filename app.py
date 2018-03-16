#!/usr/bin/python3
import json
import sys

from http_serv import HTTPServ
serv = HTTPServ()

from views import *
from models import *
session_store = Store("janky key")
appdata = Messenger()

def main():
    port = sys.argv[1] if len(sys.argv) > 1 else 8080

    serv.listen_and_serve(port=port)

if __name__ == "__main__":
    main()
