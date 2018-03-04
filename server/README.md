Example: 

```python
#!/usr/bin/python3
from http_serv import HTTPServ

def another_page(req, resp):
    resp.write("This is another page!")

def index(req, resp):
    resp.write("Hello world!")

serv = HTTPServ()
serv.handle("/another_page", another_page)
serv.handle("/", index)
serv.listen_and_serve(":8081")
```
