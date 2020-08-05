import socket
import select

def tcp_connect(address, port, connection_timeout=10):
    outgoing_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    outgoing_socket.settimeout(connection_timeout)
    outgoing_socket.connect((address, port))
    return outgoing_socket

def socket_transfer(client_socket, outgoing_socket, max_request_len=1024):
    client_bytes = 0
    incoming_bytes  = 0
    while True:
        read_ready, _, _ = select.select([client_socket, outgoing_socket], [], [])
        for s in read_ready:
            buf = s.recv(max_request_len)
            if len(buf) == 0:
                return client_bytes, incoming_bytes

            if s is client_socket:
                client_bytes += len(buf)
                outgoing_socket.sendall(buf)
            else:
                incoming_bytes += len(buf)
                client_socket.sendall(buf)
