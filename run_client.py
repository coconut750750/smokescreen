import argparse
import threading
from tkinter import Tk

from client.client import Proxy
from client.ui.main import Main
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

def start_connection(server_ip, server_port):
    args = parser.parse_args()
    logger = sslogger.ColoredLogger('root')

    args.server_ip = server_ip
    args.server_port = server_port
    
    s = Proxy(args, logger)
    proxy_thread = threading.Thread(target=s.start)
    proxy_thread.setDaemon(True)
    proxy_thread.start()

if __name__ == '__main__':
    root = Tk()
    main = Main(root, start_connection)
    root.mainloop()
