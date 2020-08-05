import logging
import re

#The background is set with 40 plus the number of the color, and the foreground with 30
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(30, 38)

#These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;{}m"
BOLD_SEQ = "\033[1m"


COLORS = {
    'WARNING': YELLOW,
    'INFO': GREEN,
    'DEBUG': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED
}

HTTP_METHOD_COLOR = MAGENTA

def color_text(text, color=WHITE, bold=False):
    return f'{BOLD_SEQ if bold else ""}{COLOR_SEQ.format(color)}{text}{RESET_SEQ}'

def color_http_method(text):
    return color_text(text, color=HTTP_METHOD_COLOR)

class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        if self.use_color and record.levelname in COLORS:
            record.levelname = color_text(record.levelname, color=COLORS[record.levelname])

        return logging.Formatter.format(self, record)

class ColoredLogger(logging.Logger):
    FORMAT = f"[{color_text('%(name)-20s', color=CYAN, bold=True)}][%(levelname)-18s]   %(message)s"
    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.DEBUG)                

        color_formatter = ColoredFormatter(self.FORMAT)

        console = logging.StreamHandler()
        console.setFormatter(color_formatter)

        self.addHandler(console)

    def log_received_http_req(self, protocol, method, address, port):
        self.debug(f"received {color_http_method(f'{protocol} {method}')} to {address}:{port}")

    def log_finished_http_req(self, protocol, method, client_bytes, incoming_bytes):
        self.debug(f"finished {color_http_method(f'{protocol} {method}')} transfering {client_bytes}b and recieving {incoming_bytes}b")
        