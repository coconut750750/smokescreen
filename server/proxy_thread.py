import socket
import select
from urllib.parse import urlparse

CONNECT = 'CONNECT'
CONNECT_SUCCESS = b'HTTP/1.1 200 OK\r\n\r\n'

def get_ip_port(method, url):
    parsed_uri = urlparse(url)
    netloc = parsed_uri.netloc
    if method == CONNECT:
        netloc = url
    
    if ':' in netloc:
        address, port = netloc.split(':')
    else:
        address = netloc
        port = 80
    return address, int(port)

def pthread(client_socket, client_addr, sslogger, max_request_len=1024, connection_timeout=10):
    request = client_socket.recv(max_request_len).decode()
    lines = request.split('\r\n')
    client_addr_str = f'{client_addr[0]}:{client_addr[1]}'

    method, url, protocol = lines[0].split()
    address, port = get_ip_port(method, url)

    sslogger.log_received_http_req(protocol, method, address, port)
    
    try:
        outgoing_socket = connect(address, port, connection_timeout)
    except Exception as e:
        sslogger.error(f"failed to connect error: {e}")
        client_socket.close()
        return

    try:
        if method == CONNECT:
            client_socket.sendall(CONNECT_SUCCESS)
        else:
            outgoing_socket.sendall(request.encode())

        client_bytes, incoming_bytes = transfer(client_socket, outgoing_socket, max_request_len)

        sslogger.log_finished_http_req(protocol, method, client_bytes, incoming_bytes)
    except Exception as e:
        sslogger.error(f"transfer failed: {e}")
    finally:
        client_socket.close()
        outgoing_socket.close()

def connect(address, port, connection_timeout=10):
    outgoing_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    outgoing_socket.settimeout(connection_timeout)
    outgoing_socket.connect((address, port))
    return outgoing_socket

def transfer(client_socket, outgoing_socket, max_request_len=1024):
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
