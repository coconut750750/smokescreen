import argparse

from server.server import Server
from server.config import ServerConfig
import lib.sslogger as sslogger

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
parser.add_argument('--no-enc', dest='encrypted', action='store_const',
                    const=False, default=True,
                    help='Client won\'t establish encrypted connection')


if __name__ == '__main__':
    args = parser.parse_args()

    config = ServerConfig(
        args.hostname,
        args.port,
        args.buffer,
        args.timeout,
        args.encrypted,
    )

    s = Server(config, sslogger.ColoredLogger('root'))
    s.start()