from lib.ssocket import tcp_connect, socket_transfer
from lib.crypto.dhe import client_dhe_request, client_dhe_finish
from lib.crypto.aes import aes_encrypt, aes_decrypt

VPN_CONNECTION_LENGTH = 1024

class ClientConnection:
    def __init__(self, client_socket, client_addr, server, logger, max_request_len=1024, connection_timeout=10):
        self.client_socket = client_socket
        self.client_addr = client_addr
        self.client_addr_str = f'{client_addr[0]}:{client_addr[1]}'
        self.server = server
        self.logger = logger
        self.max_request_len = max_request_len
        self.connection_timeout = connection_timeout
        self.vpn_socket = None
        self.shared_key = None

    def vpn_connect(self):
        self.vpn_socket = tcp_connect(*self.server, connection_timeout=self.connection_timeout)
        private_key, request = client_dhe_request()
        self.vpn_socket.sendall(request)
        server_resp = self.vpn_socket.recv(VPN_CONNECTION_LENGTH)
        self.shared_key = client_dhe_finish(private_key, server_resp)

    def run(self):
        try:
            self.vpn_connect()
        except Exception as e:
            self.logger.error(f"failed to connect to server error: {e}")
            self.client_socket.close()
            return

        try:
            self.logger.info(f"starting connection")
            client_bytes, incoming_bytes = socket_transfer(self.client_socket, self.vpn_socket, max_request_len=self.max_request_len)
            self.logger.info(f"closing connection")
        except Exception as e:
            self.logger.error(f"transfer failed: {e}")
        finally:
            self.client_socket.close()
            self.vpn_socket.close()
