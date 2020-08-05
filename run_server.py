import argparse
import sys

from server import Server
import sslogger

parser = argparse.ArgumentParser(description='Runs a Smokescreen VPN server.')
parser.add_argument('--hostname', metavar='HOSTNAME', type=str,
                    default='localhost',
                    help='Default: localhost. Server IP address.')
parser.add_argument('--port', '-p', metavar='PORT', type=int,
                    default=1515,
                    help='Default: 1515. Server port.')
parser.add_argument('--buffer', metavar='BUFFER_SIZE', type=int,
                    default=1000000,
                    help='Default: 1MB. Size of the buffer.')
parser.add_argument('--timeout', metavar='TIMEOUT', type=int,
                    default=10,
                    help='Default: 10. Socket timeout in seconds.')

if __name__ == '__main__':
    args = parser.parse_args()

    s = Server(args, sslogger.ColoredLogger('root'))
    s.start()