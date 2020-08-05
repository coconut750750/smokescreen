import socket
import select

def tcp_connect(address, port, connection_timeout=10):
    outgoing_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    outgoing_socket.settimeout(connection_timeout)
    outgoing_socket.connect((address, port))
    return outgoing_socket
