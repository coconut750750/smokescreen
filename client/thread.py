from lib.ssocket import tcp_connect, socket_transfer
from lib.crypto.dhe import client_dhe_request, client_dhe_finish

VPN_CONNECTION_LENGTH = 1024

def vpn_connect(address, port, connection_timeout=10):
    vpn_socket = tcp_connect(address, port, connection_timeout=connection_timeout)
    private_key, request = client_dhe_request()
    vpn_socket.sendall(request)
    server_resp = vpn_socket.recv(VPN_CONNECTION_LENGTH)
    shared_key = client_dhe_finish(private_key, server_resp)

    return vpn_socket, shared_key

def pthread(client_socket, client_addr, server, logger, max_request_len=1024, connection_timeout=10):
    client_addr_str = f'{client_addr[0]}:{client_addr[1]}'
    
    try:
        vpn_socket, shared_key = vpn_connect(*server, connection_timeout=connection_timeout)
    except Exception as e:
        logger.error(f"failed to connect to server error: {e}")
        client_socket.close()
        return

    try:
        logger.info(f"starting connection")
        client_bytes, incoming_bytes = socket_transfer(client_socket, vpn_socket, max_request_len=max_request_len)
        logger.info(f"closing connection")
    except Exception as e:
        logger.error(f"transfer failed: {e}")
    finally:
        client_socket.close()
        vpn_socket.close()
