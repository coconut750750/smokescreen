from lib.ssocket import tcp_connect, socket_transfer

def pthread(client_socket, client_addr, server, logger, max_request_len=1024, connection_timeout=10):
    client_addr_str = f'{client_addr[0]}:{client_addr[1]}'
    
    try:
        vpn_socket = tcp_connect(*server, connection_timeout=connection_timeout)
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

