from socket import socket
import struct

from authentication_methods import AuthenticationMethods
from connection_state import ConnectionState
from constants import AUTHENTICATION_HEADER_SIZE
from socks_parser import SocksParser
from socks_version import SocksVersion
from utils import receive_all


class AuthenticationHandler:
    def __init__(self, parser: SocksParser):
        self.parser: SocksParser = parser

    def handle(self, client_socket: socket, socks_version: SocksVersion):
        """
        Handles method-dependent subnegotiation, validates authentication message
        and, selects authentication method.
        """
        header = receive_all(client_socket, AUTHENTICATION_HEADER_SIZE)
        try:
            client_version, nmethods = header
            methods = receive_all(client_socket, nmethods)
            accepted_method = self.parser.select_method(
                client_version, 
                methods, 
                socks_version, 
                [AuthenticationMethods.NO_AUTHENTICATION.value]
            )
        except ValueError as excpetion:
            return ConnectionState.CLOSED
        client_socket.sendall(struct.pack("BB", socks_version.value, accepted_method))
        if AuthenticationMethods.NO_ACCEPTABLE_METHODS.value == accepted_method:
            return ConnectionState.CLOSED
        return ConnectionState.REQUEST