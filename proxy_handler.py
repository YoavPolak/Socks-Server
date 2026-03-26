from socket import socket
from select import select

from connection_state import ConnectionState

class ProxyHandler:
    def handle(self, client_socket: socket, destination_socket: socket):
        """
        Tunneling between two sockets.
        :param client_socket: The clients socket.
        :param destination_socket: The destination socket.
        :return connection state (CLOSED)
        """
        sockets = [client_socket, destination_socket]
        signal = True
        while signal:
            readables, writables, exceptionals = select(sockets, [], [])
            for socket in readables:
                data = socket.recv(1024)
                if not data:
                    signal = False
                if socket is client_socket:
                    destination_socket.sendall(data)
                else:
                    client_socket.sendall(data)
        return ConnectionState.CLOSED