import threading
import tkinter
import lib.sslogger as sslogger

from client.client import Proxy
from client.ui.start import Start
from client.ui.connected import Connected

class App(object):
    def __init__(self, config):
        self.root = tkinter.Tk()
        self.config = config
        self.proxy = None
        self.proxy_thread = None

        # widgets
        self.main = None
        self.connected = None

    def start_connection(self, server_ip, server_port):
        logger = sslogger.ColoredLogger('root')

        self.config.server_ip = server_ip
        self.config.server_port = server_port
        
        self.proxy = Proxy(self.config, logger)
        self.proxy_thread = threading.Thread(target=self.proxy.start)
        self.proxy_thread.setDaemon(True)
        self.proxy_thread.start()

        self.main.pack_forget()
        self.render_connected(server_ip, server_port)
        
    def end_connection(self):
        self.proxy.disconnect()
        self.proxy_thread.join()
        self.connected.pack_forget()
        self.render_start()

    def start(self):
        self.render_start()
        self.root.winfo_toplevel().title("Smokescreen")
        self.root.mainloop()

    def render_start(self):
        self.main = Start(self.root, self.start_connection)
        self.main.pack()

    def render_connected(self, server_ip, server_port):
        self.connected = Connected(self.root, f'{server_ip}:{server_port}', self.end_connection)
        self.connected.pack()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.proxy:
            self.proxy.disconnect()
