from socket import AF_INET, AF_INET6, inet_pton
import struct

from address_type import AddressType
from socks_packet import SocksResponse


class ResponseSerializer:

    def to_bytes(self, response: SocksResponse) -> bytes:
        """
        Serialize SocksResponse to bytes.
        :param response: response in SocksResponse structure.
        :return socks response in bytes.
        """
        address = self._address_to_bytes(response.atyp, response.address)
        return struct.pack("BBBB", response.version.value, response.reply.value, 0, response.atyp.value) + address
    
    def _address_to_bytes(self, address_type: AddressType, address: tuple[str, int]) -> bytes:
        """
        Serialize address to bytes.
        :param address_type: Address type.
        :param address: tuple of address and port.
        :return: packed address and port.
        """
        match address_type:
            case AddressType.IPV4:
                packed_address = inet_pton(AF_INET, address[0])
            case AddressType.IPV6:
                packed_address = inet_pton(AF_INET6, address[0])
            case AddressType.DOMAIN:
                domain = address[0].encode()
                packed_address = struct.pack("B", len(domain)) + domain
        packed_port = struct.pack("!H", address[1])
        return packed_address + packed_port