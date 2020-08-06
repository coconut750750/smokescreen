import threading
import tkinter
import lib.sslogger as sslogger

from client.client import Proxy
from client.ui.main import Main

class App(object):
    def __init__(self, config):
        self.root = tkinter.Tk()
        self.config = config

    def start_connection(self, server_ip, server_port):
        logger = sslogger.ColoredLogger('root')

        self.config.server_ip = server_ip
        self.config.server_port = server_port
        
        self.proxy = Proxy(self.config, logger)
        proxy_thread = threading.Thread(target=self.proxy.start)
        proxy_thread.setDaemon(True)
        proxy_thread.start()

    def start(self):
        main = Main(self.root, self.start_connection)
        self.root.mainloop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.proxy.disconnect()
