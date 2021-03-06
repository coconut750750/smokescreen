import socket
import signal
import threading
import lib.sslogger as sslogger

from server.vpn_connection import VPNConnection

class Server:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

        signal.signal(signal.SIGINT, self.shutdown) 

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((config.hostname, config.port))

        self.logger.info(f"starting smokescreen on {config.hostname}:{config.port}")
        
        self.server_socket.listen(10)
        # self.__clients = {}

    def shutdown(self, signum, frame):
        """ Handle the exiting server. Clean all traces """
        self.logger.info('Shutting down gracefully...')
        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is main_thread:
                continue
            t.join()
        self.server_socket.close()

    def _getClientName(self, addr):
        return f'ssc-{addr[0]}:{addr[1]}'

    def start(self):
        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                self.logger.info(f'recieved client at {client_address}')
                
                thread_name = self._getClientName(client_address)
                connection = VPNConnection(
                    client_socket,
                    client_address,
                    sslogger.ColoredLogger(thread_name),
                    max_request_len=self.config.buffer_size,
                    connection_timeout=self.config.timeout,
                    encrypted=self.config.encrypted,
                )

                c = threading.Thread(name=thread_name, target=connection.run)
                c.setDaemon(True)
                c.start()
            except Exception as e:
                self.logger.error(e)
                break
