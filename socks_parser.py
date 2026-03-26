from typing import List

from address_type import AddressType
from invalid_socks_request import InvalidSocksRequest
from reply_field import ReplyField
from socks_command import SocksCommand
from socks_packet import SocksRequest
from socks_version import SocksVersion
from authentication_methods import AuthenticationMethods

class SocksParser:
    def select_method(self, client_version: int, client_methods: bytes, server_version: SocksVersion, server_methods: List[AuthenticationMethods]):
        """
        Validates whether the authentication packet is valid and compatable with the server
        :param client_version: Client's Socks version from the header.
        :param client_methods: Client's authetication methods.
        :param server_version: Server's Socks version.
        :param server_methods: Server's supported authetication methods.
        :return: Selected method for authentication with client.
        """
        if client_version != server_version.value:
            raise ValueError("Malformed Socks packet.")
        for method in client_methods:
            if method in server_methods:
                return method
        return AuthenticationMethods.NO_ACCEPTABLE_METHODS.value
    
    def parse_request_header(self, header: bytes, server_version: SocksVersion):
        """
        Parse Socks request header and validates the request header.
        :param header: Socks request header.
        :param server_version: Server's Socks version.
        :return SocksRequest.
        """
        client_version, cmd, _, atyp = header
        if server_version.value != client_version:
            raise InvalidSocksRequest("Invalid SOCKS version.", reply=ReplyField.INVALID_SOCKS_VERSION)
        supported_commands = [command.value for command in SocksCommand]
        if cmd not in supported_commands:
            raise InvalidSocksRequest("Unsupoorted command", reply=ReplyField.COMMAND_NOT_SUPPORTED)
        supported_address_types = [address_type.value for address_type in AddressType]
        if atyp not in supported_address_types:
            raise InvalidSocksRequest("Unsupported address type", reply=ReplyField.ATYP_NOT_SUPPORTED)
        return SocksRequest(atyp=AddressType(atyp), command=SocksCommand(cmd))