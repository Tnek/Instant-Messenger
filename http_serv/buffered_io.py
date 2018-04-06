import os.path

class FileBuffer(object):
    """ Buffered file I/O that conforms to the interface defined here """
    def __init__(self, directory):
        self.file_dir = directory
        self.file_hand = None

    def read(self, nbytes):
        if self.file_hand == None:
            self.file_hand = open(self.file_dir, "rb")

        return self.file_hand.read(nbytes)
    
    def close(self):
        self.file_hand.close()
        self.file_hand = None
        
    def size(self):
        return os.path.getsize(self.file_dir)


class StringBuffer(object):
    """ io.StringIO is blocking, but we need it to be nonblocking """
    def __init__(self, initial=b''):
        self.chr_arr = bytearray(initial)

    def write(self, s):
        for c in s:
            self.chr_arr.append(ord(c))
    
    def read(self, nbytes):
        ret = self.chr_arr[:nbytes]
        self.chr_arr = self.chr_arr[nbytes:]
        return ret

    def values(self):
        return self.chr_arr.decode("utf-8")

    def close(self):
        pass


class BufferedIO(object):
    """ 
            We use this instead of the builtin Python io module or 
        socket.makefile() because those cause the socket to switch to nonblocking
        mode, which means we can't do persistent HTTP.
    """
    def __init__(self, read_func, write_func):
        self.buf = []
        self.write_func = write_func
        self.read_func = read_func

    def fetch_more(self, chunk_size=1024):
        if len(self.buf) <= 0:
            data = self.read_func(chunk_size)
            for c in data:
                self.buf.append(chr(c))

    def read_until(self, stop):
        builder = []
        while True:
            self.fetch_more()
            
            for c in range(len(self.buf)):
                builder.append(self.buf[c])
                if self.buf[c] == stop:
                    self.buf = self.buf[c+1:]
                    return "".join(builder)

    def read(self, nbytes):
        if nbytes > len(self.buf):
            for c in self.read_func(nbytes - len(self.buf)):
                self.buf.append(chr(c))

        ret = self.buf[:nbytes]
        self.buf = self.buf[nbytes:]
        return "".join(ret)

    def buf_write(self, stream, chunk_size=1024):
        d = stream.read(chunk_size)
        while d:
            self.write_func(d)
            d = stream.read(chunk_size)
        stream.close()

