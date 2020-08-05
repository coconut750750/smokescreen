import argparse

from client import Proxy
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

if __name__ == '__main__':
    args = parser.parse_args()

    s = Proxy(args, sslogger.ColoredLogger('root'))
    s.start()