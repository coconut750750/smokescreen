import argparse
import wx
import threading

from client.client import Proxy
from client.ui.main import MainWindow
import lib.sslogger as sslogger

parser = argparse.ArgumentParser(description='Runs a Smokescreen VPN client.')
parser.add_argument('--server-ip', '-s', metavar='SERVER_IP', type=str,
                    default='localhost',
                    help='Default: localhost. Server IP.')
parser.add_argument('--server-port', '-p', metavar='SERVER_PORT', type=int,
                    default=1515,
                    help='Default: 1515. Server port.')
parser.add_argument('--client-port', metavar='PORT', type=int,
                    default=1516,
                    help='Default: 1516. Client port.')
parser.add_argument('--buffer', metavar='BUFFER_SIZE', type=int,
                    default=1000000,
                    help='Default: 1MB. Size of the buffer.')
parser.add_argument('--timeout', metavar='TIMEOUT', type=int,
                    default=10,
                    help='Default: 10. Socket timeout in seconds.')

def start_connection(window, server_ip, server_port):
    args = parser.parse_args()
    uihandler = sslogger.SSHandler(lambda r: window.add_log(r.asctime, r.levelname, r.message))
    logger = sslogger.ColoredLogger('root')
    logger.addHandler(uihandler)

    args.server_ip = server_ip
    args.server_port = server_port
    
    s = Proxy(args, logger)
    proxy_thread = threading.Thread(target=s.start)
    proxy_thread.setDaemon(True)
    proxy_thread.start()

if __name__ == '__main__':
    app = wx.App(False)
    window = MainWindow(start_connection)
    app.MainLoop()