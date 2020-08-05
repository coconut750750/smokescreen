import socket
import select

def tcp_connect(address, port, connection_timeout=10):
    outgoing_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    outgoing_socket.settimeout(connection_timeout)
    outgoing_socket.connect((address, port))
    return outgoing_socket

def transfer_all(insock, outsock, max_request_len=1024):
    n_bytes = 0
    read_ready = [insock]

    while len(read_ready) > 0:
        buf = insock.recv(max_request_len)
        if len(buf) == 0:
            return n_bytes, False
    
        n_bytes += len(buf)
        outsock.sendall(buf)
        read_ready, _, _ = select.select([insock], [], [], 0)
    
    return n_bytes, True

def socket_transfer(client_socket, outgoing_socket, max_request_len=1024):
    client_bytes = 0
    incoming_bytes  = 0
    while True:
        read_ready, _, _ = select.select([client_socket, outgoing_socket], [], [])
        for s in read_ready:
            if s is client_socket:
                n_bytes, socket_open = transfer_all(s, outgoing_socket, max_request_len=max_request_len)
                client_bytes += n_bytes
            else:
                n_bytes, socket_open = transfer_all(s, client_socket, max_request_len=max_request_len)
                incoming_bytes += n_bytes

            if not socket_open:
                return client_bytes, incoming_bytes
