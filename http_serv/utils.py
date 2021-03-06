#!/usr/bin/python

# RFC 3986 section 2.2 Reserved Characters (January 2005)
urlenc_reserved_chars = {"!","*","'", "(", ")", ";", ":", "@", "&", "=", "+", "$", ",", "/", "?", "#", "[", "]", " "}

def urlencode(s):
    build = []
    for c in s:
        if c in urlenc_reserved_chars:
            build.append("%")
            build.append(hex(ord(c))[2:].upper())
        else:
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

        if s[cur] == "+":
            build.append(" ")
        else: 
            build.append(s[cur])
        cur += 1


    return "".join(build)

html_extra_escaped_chrs = {"'", "`", "!", "@", "$", "%", "(", ")", "=", "+", "{", "}", "[", "]"}
html_escape_chrs = {
        "&":"&amp;",
        "<":"&lt;", 
        ">":"&gt;", 
        '"':"&quot;"
}
html_escape_chrs.update({i:"&#"+str(ord(i))+";" for i in html_extra_escaped_chrs})

def html_escape(s):
    build = []
    for c in s:
        if c in html_escape_chrs:
            build.append(html_escape_chrs[c])
        else:
            build.append(c)
    return "".join(build)
