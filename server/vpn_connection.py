from urllib.parse import urlparse

from lib.ssocket import tcp_connect
from lib.ssocket.ssocket import TransferSocket
from lib.crypto.dhe import server_dhe_response
from lib.crypto.aes import get_cryptors

VPN_CONNECTION_LENGTH = 1024
CONNECT = 'CONNECT'
CONNECT_SUCCESS = b'HTTP/1.1 200 OK\r\n\r\n'

def get_ip_port(method, url):
    parsed_uri = urlparse(url)
    netloc = parsed_uri.netloc
    if method == CONNECT:
        netloc = url
    
    if ':' in netloc:
        address, port = netloc.split(':')
    else:
        address = netloc
        port = 80
    return address, int(port)

class VPNConnection:
    def __init__(self, client_socket, client_addr, sslogger, max_request_len=1024, connection_timeout=10, encrypted=True):
        self.client_socket = client_socket
        self.client_addr = client_addr
        self.sslogger = sslogger
        self.max_request_len = max_request_len
        self.connection_timeout = connection_timeout
        self.encrypted = encrypted
        self.outgoing_socket = None
        self.encryptor = None
        self.decryptor = None

    def setup_connection(self):
        client_req = self.client_socket.recv(VPN_CONNECTION_LENGTH)
        shared_key, server_response = server_dhe_response(client_req)
        self.client_socket.sendall(server_response)
        self.encryptor, self.decryptor = get_cryptors(shared_key)

    def client_recv(self):
        buf = self.client_socket.recv(self.max_request_len)
        if self.encrypted:
            return self.decryptor.update(buf).decode()
        return buf.decode()

    def client_send(self, buf):
        if self.encrypted:
            return self.client_socket.sendall(self.encryptor.update(buf))
        return self.client_socket.sendall(buf)

    def transform_client_bytes(self, b):
        if self.encrypted:
            return self.decryptor.update(b)
        return b

    def transform_incoming_bytes(self, b):
        if self.encrypted:
            return self.encryptor.update(b)
        return b

    def run(self):
        if self.encrypted:
            self.setup_connection()

        request = self.client_recv()
        lines = request.split('\r\n')
        method, url, protocol = lines[0].split()
        address, port = get_ip_port(method, url)

        self.sslogger.log_received_http_req(protocol, method, address, port)
        
        try:
            self.outgoing_socket = tcp_connect(address, port, connection_timeout=self.connection_timeout)
        except Exception as e:
            self.sslogger.error(f"failed to connect error: {e}")
            self.client_socket.close()
            return

        try:
            transfer_socket = TransferSocket(
                self.client_socket,
                self.outgoing_socket,
                self.transform_client_bytes,
                self.transform_incoming_bytes,
                max_request_len=self.max_request_len
            )

            if method == CONNECT:
                self.client_send(CONNECT_SUCCESS)
            else:
                self.outgoing_socket.sendall(request.encode())

            client_bytes, incoming_bytes = transfer_socket.run()

            self.sslogger.log_finished_http_req(protocol, method, client_bytes, incoming_bytes)
        except Exception as e:
            self.sslogger.error(f"transfer failed: {e}")
        finally:
            self.client_socket.close()
            self.outgoing_socket.close()
