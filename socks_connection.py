from socket import socket

from authentication_handler import AuthenticationHandler
from connection_state import ConnectionState
from request_handler import RequestHandler
from proxy_handler import ProxyHandler
from socks_version import SocksVersion

class SocksConnection:
    def __init__(
        self, 
        client_socket: socket, 
        state: ConnectionState, 
        authentication_handler: AuthenticationHandler,
        request_handler: RequestHandler,
        proxy_handler: ProxyHandler,
        socks_version: SocksVersion = SocksVersion.FIVE,
    ):
        self.client_socket = client_socket
        self.state: ConnectionState = state
        self.authentication_handler: AuthenticationHandler = authentication_handler
        self.request_handler: RequestHandler = request_handler
        self.proxy_handler: ProxyHandler = proxy_handler
        self.destination_socket: socket = None
        self.socks_version = socks_version

    def handle(self):
        """
        Handles the socks connection with the client.
        """
        signal = True
        while signal:
            match self.state:
                case ConnectionState.AUTHENTICATION:
                    self.state = self.authentication_handler.handle(self.client_socket, self.socks_version)
                case ConnectionState.REQUEST:
                    self.state, self.destination_socket = self.request_handler.handle(self.client_socket, self.socks_version)
                case ConnectionState.PROXY:
                    self.state = self.proxy_handler.handle(self.client_socket, self.destination_socket)
                case ConnectionState.CLOSED:
                    signal = False
        self._close_sockets()
    
    def _close_sockets(self):
        """
        Closes connection between destination socket if exists
        and closes connection with client.
        """
        self.client_socket.close()
        if self.destination_socket:
            self.destination_socket.close()
