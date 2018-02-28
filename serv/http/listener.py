#!/usr/bin/python

import socket
from tokenizer import Tokenizer

class HTTPServ(object):
    def __init__(self):
        pass

    def listen_and_serve(self, serv_addr):
        host, port = serv_addr.split(":")
        if host == "":
            self.host = "0.0.0.0"
        if port == "http":
            port = 80
        self.port = int(port)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(5)

        while True:
            tokenizer = Tokenizer()
            client, addr = sock.accept()

            buf = client.recv(1024)
            while tokenizer.tokenize_buf(buf):
                pass
            
            client.send("test")

            for i in tokenizer.export_tokens():
                print(i)
        sock.close()


def test():
    serv = HTTPServ()
    serv.listen_and_serve(":8080")

if __name__ == "__main__":
    test()
