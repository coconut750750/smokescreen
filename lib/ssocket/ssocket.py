import socket
import select

class TransferSocket:
    def __init__(self, client_socket, server_socket, transform_client_recv, transform_server_recv, max_request_len=1024):
        self.client_socket = client_socket
        self.server_socket = server_socket
        self.transform_client_recv = transform_client_recv
        self.transform_server_recv = transform_server_recv
        self.max_request_len = max_request_len

        self.client_bytes = 0
        self.server_bytes = 0

    def forward_bytes(self, from_sock, to_sock, transform):
        in_buf = from_sock.recv(self.max_request_len)
        if len(in_buf) == 0:
            return 0
        out_buf = transform(in_buf)
        to_sock.sendall(out_buf)
        return len(in_buf)

    def run(self):
        while True:
            read_ready, _, _ = select.select([self.client_socket, self.server_socket], [], [])
            for s in read_ready:
                if s is self.client_socket:
                    bytes_recv = self.forward_bytes(s, self.server_socket, self.transform_client_recv)
                    self.client_bytes += bytes_recv
                else:
                    bytes_recv = self.forward_bytes(s, self.client_socket, self.transform_server_recv)
                    self.server_bytes += bytes_recv

                if bytes_recv == 0:
                    return self.client_bytes, self.server_bytes
