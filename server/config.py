class ServerConfig:
    def __init__(self, hostname, port, buffer_size, timeout, encrypted):
        self.hostname = hostname
        self.port = port
        self.buffer_size = buffer_size
        self.timeout = timeout
        self.encrypted = encrypted
