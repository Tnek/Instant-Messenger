# http_serv

http_serv is an HTTP server and web application framework.

## A Simple Example

```
#!/usr/bin/python3
from http_serv import HTTPServ

def index(req, resp):
    resp.write("Hello world!")

serv = HTTPServ()
serv.handle("/", index)
serv.listen_and_serve(port=8080)
```
