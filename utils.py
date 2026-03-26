from socket import socket

def receive_all(socket: socket, size: int) -> bytes:
    """
    Reads data from socket.
    :param socket: socket to read from.
    :param size: Size of data to read
    :return: data from socket
    """
    if 0 >= size:
        return b""
    data = b""
    while len(data) < size:
        chunk = socket.recv(size - len(data))
        if not chunk:
            return data
        data += chunk
    return data