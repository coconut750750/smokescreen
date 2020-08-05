from urllib.parse import urlparse

from lib.ssocket import tcp_connect, socket_transfer

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
        outgoing_socket = tcp_connect(address, port, connection_timeout=connection_timeout)
    except Exception as e:
        sslogger.error(f"failed to connect error: {e}")
        client_socket.close()
        return

    try:
        if method == CONNECT:
            client_socket.sendall(CONNECT_SUCCESS)
        else:
            outgoing_socket.sendall(request.encode())

        client_bytes, incoming_bytes = socket_transfer(client_socket, outgoing_socket, max_request_len=max_request_len)

        sslogger.log_finished_http_req(protocol, method, client_bytes, incoming_bytes)
    except Exception as e:
        sslogger.error(f"transfer failed: {e}")
    finally:
        client_socket.close()
        outgoing_socket.close()
