from socket import AF_INET, AF_INET6, inet_ntop, socket

from address_type import AddressType
from constants import DOMAIN_SIZE_FIELD, IPV4_SIZE, IPV6_SIZE, PORT_SIZE
from utils import receive_all


class AddressReader:
    def read(self, client_socket: socket, address_type: AddressType) -> tuple[str, int] | None:
        """
        Receiving an address from socks packet.
        :param client_socket: The client's socket.
        :param address_type: The address type of the address sent by the client.
        :return address tuple (ip/domain, port).
        """
        match address_type:
            case AddressType.IPV4:
                address = self._receive_ip4(client_socket)
            case AddressType.DOMAINNAME:
                address = self._receive_domain(client_socket)
            case AddressType.IPV6:
                address = self._receive_ip6(client_socket)
            case _:
                return None
        port_bytes = receive_all(client_socket, PORT_SIZE)
        port = int.from_bytes(port_bytes, byteorder="big")
        return address, port
    
    def _receive_ip4(self, client_socket) -> str:
        """
        Reads IPv4 address from socket and converts it into
        address format.
        :param client_socket: The client's socket
        :return: IPv4 in string format
        """
        data = receive_all(client_socket, IPV4_SIZE)
        return inet_ntop(AF_INET ,data)
    
    def _receive_ip6(self, client_socket) -> str:
        """
        Reads IPv6 address from socket and converts it into
        address format.
        :param client_socket: The client's socket
        :return: IPv6 in string format
        """
        data = receive_all(client_socket, IPV6_SIZE)
        return inet_ntop(AF_INET6 ,data)
    
    def _receive_domain(self, client_socket) -> str:
        """
        Reads domain name from socket and converts it into
        address format.
        :param client_socket: The client's socket
        :return: Domain name in string format.
        """
        domain_length = receive_all(client_socket, DOMAIN_SIZE_FIELD)
        domain = receive_all(client_socket, domain_length[0])
        return domain.decode()