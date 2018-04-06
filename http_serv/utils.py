#!/usr/bin/python
# RFC 3986 section 2.2 Reserved Characters (January 2005)
reserved_chars = {"!","*","'", "(", ")", ";", ":", "@", "&", "=", "+", "$", ",", "/", "?", "#", "[", "]"}

def urlencode(s):
    build = []
    for c in s:
        if c in reserved_chars:
            build.append("%")
            build.append(hex(ord(c))[2:].upper())
            continue
        build.append(c)
    return "".join(build)

def urldecode(s):
    build = []
    cur = 0
    s_len = len(s)

    while cur < s_len:
        if s[cur] == "%":
            c = chr(int(s[cur+1:cur+3], 16))
            build.append(c)
            cur += 3
            continue

        build.append(s[cur])
        cur += 1

    return "".join(build)
