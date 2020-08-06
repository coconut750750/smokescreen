import socket
import signal
import threading
import lib.sslogger as sslogger

from client.client_connection import ClientConnection

HOSTNAME = 'localhost'

class Proxy:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.server = (config.server_ip, config.server_port)

        signal.signal(signal.SIGINT, self.disconnect) 

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((HOSTNAME, config.client_port))

        self.logger.info(f"starting smokescreen on {HOSTNAME}:{config.client_port}")
        
        self.server_socket.listen(10)
        self.connections = {} # port : client connection object

    def disconnect(self, signum, frame):
        self.logger.info('Shutting down gracefully...')
        for port, connection in self.connections.items():
            connection.end()

        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is main_thread:
                continue
            t.join()
        self.server_socket.close()

    def format_client_name(self, addr):
        return f'phc-{addr[0]}:{addr[1]}'

    def connection_ended(self, port):
        if port in self.connections:
            del self.connections[port]

    def start(self):
        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                client_port = client_address[1]
                self.logger.info(f'recieved client at {client_address}')
                
                thread_name = self.format_client_name(client_address)
                connection = ClientConnection(
                    client_socket,
                    client_address,
                    self.server,
                    sslogger.ColoredLogger(thread_name),
                    lambda: self.connection_ended(client_port),
                    max_request_len=self.config.buffer,
                    connection_timeout=self.config.timeout
                )
                self.connections[client_port] = connection

                c = threading.Thread(
                    name=thread_name,
                    target=connection.run,
                )
                c.setDaemon(True)
                c.start()
            except Exception as e:
                self.logger.error(e)
                break
