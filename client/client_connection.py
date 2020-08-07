from lib.ssocket import tcp_connect
from lib.ssocket.ssocket import TransferSocket

from lib.crypto.dhe import client_dhe_request, client_dhe_finish
from lib.crypto.aes import get_cryptors

VPN_CONNECTION_LENGTH = 1024

class ClientConnection:
    def __init__(self, client_socket, client_addr, server, sslogger, cleanup, max_request_len=1024, connection_timeout=10):
        self.client_socket = client_socket
        self.client_ip = client_addr[0]
        self.client_port = client_addr[1]
        self.client_addr_str = f'{self.client_ip}:{self.client_port}'
        self.server = server
        self.sslogger = sslogger
        self.max_request_len = max_request_len
        self.connection_timeout = connection_timeout
        self.cleanup = cleanup
        self.vpn_socket = None
        self.encryptor = None
        self.decryptor = None

    def vpn_connect(self):
        self.vpn_socket = tcp_connect(*self.server, connection_timeout=self.connection_timeout)
        private_key, request = client_dhe_request()
        self.vpn_socket.sendall(request)
        server_resp = self.vpn_socket.recv(VPN_CONNECTION_LENGTH)
        shared_key = client_dhe_finish(private_key, server_resp)
        self.encryptor, self.decryptor = get_cryptors(shared_key)

    def end(self):
        self.client_socket.close()
        if self.vpn_socket:
            self.vpn_socket.close()

    def run(self):
        try:
            self.vpn_connect()
        except Exception as e:
            self.sslogger.error(f"failed to connect to server error: {e}")
            self.client_socket.close()
            self.cleanup(self.client_port)
            return

        try:
            transfer_socket = TransferSocket(
                self.client_socket,
                self.vpn_socket,
                lambda b: self.encryptor.update(b),
                lambda b: self.decryptor.update(b),
                max_request_len=self.max_request_len
            )

            self.sslogger.info(f"starting connection")

            client_bytes, incoming_bytes = transfer_socket.run()

            self.sslogger.info(f"closing connection")
        except Exception as e:
            self.sslogger.error(f"transfer failed: {e}")
        finally:
            self.client_socket.close()
            self.vpn_socket.close()
            self.cleanup(self.client_port)
