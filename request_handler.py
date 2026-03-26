from socket import create_connection, socket, timeout
from typing import Tuple

from address_reader import AddressReader
from connection_state import ConnectionState
from constants import REQUEST_HEADER_SIZE
from invalid_socks_request import InvalidSocksRequest
from reply_field import ReplyField
from response_serializer import ResponseSerializer
from socks_packet import SocksRequest, SocksResponse
from socks_parser import SocksParser
from socks_version import SocksVersion
from utils import receive_all

class RequestHandler:
    exceptions_to_reply_code = {
        # Maps Exceptions to reply code
        10013: ReplyField.CONNECTION_NOT_ALLOWED,
        10051: ReplyField.NETWORK_UNREACHABLE,
        10065: ReplyField.HOST_UNREACHABLE,
        10061: ReplyField.CONNECTION_REFUSED,
        10060: ReplyField.TTL_EXPIRED,
    }

    def __init__(self, parser: SocksParser, address_reader: AddressReader, response_serializer: ResponseSerializer):
        self.parser: SocksParser = parser
        self.address_reader: AddressReader = address_reader
        self.response_serializer : ResponseSerializer = response_serializer

    def handle(self, client_socket: socket, socks_version: SocksVersion):
        """
        Handles requests from client
        :param client_socket: The client sockets
        :param socks_version: The servers socks version.
        :return: Connection state and destination socket.
        """
        header = receive_all(client_socket, REQUEST_HEADER_SIZE)
        try:
            request = self.parser.parse_request_header(header, socks_version)
            request.address = self.address_reader.read(client_socket, request.atyp) 
        except InvalidSocksRequest as exception:
            if exception.reply:
                response = SocksResponse(reply=exception.reply)
                client_socket.sendall(self.response_serializer.to_bytes(response)) #TODO maybe change responder
                return ConnectionState.CLOSED, None
        except ValueError as exception:
            return ConnectionState.CLOSED, None
            
        destination_socket, response = self._connect(request)
        client_socket.sendall(self.response_serializer.to_bytes(response))
        if not destination_socket:
            return ConnectionState.CLOSED, None
        return ConnectionState.PROXY, destination_socket
    
    def _connect(self, request: SocksRequest) -> Tuple[socket, SocksResponse]:
        """
        Connect to destination server.
        :param request: Socks request
        :return tuple of destination socket and server response
        """
        try:
            destination = create_connection(request.address, timeout=5)
            return destination, SocksResponse(atyp=request.atyp, address=request.address)
        except timeout as exception:
            return None, SocksResponse(reply=ReplyField.TTL_EXPIRED)
        except OSError as exception:
            reply = self.exceptions_to_reply_code.get(exception.winerror, ReplyField.UNKNOWN_ERROR)
            return None, SocksResponse(reply=reply)