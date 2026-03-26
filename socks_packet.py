from dataclasses import dataclass
from address_type import AddressType
from constants import DEFAULT_ADDRESS
from reply_field import ReplyField
from socks_command import SocksCommand
from socks_version import SocksVersion

@dataclass
class SocksPacket:
    """
    Socks Packet with fields that always exist.
    """
    atyp: AddressType = AddressType.IPV4
    address: tuple[str, int] = DEFAULT_ADDRESS
    version: SocksVersion = SocksVersion.FIVE
    reserved: int = 0

@dataclass
class SocksRequest(SocksPacket):
    """
    Socks request
    (Extends Socks packet with command field)
    """
    command: SocksCommand = SocksCommand.CONNECT

@dataclass
class SocksResponse(SocksPacket):
    """
    Socks response
    (Extends Socks packet with reply field)
    """
    reply: ReplyField = ReplyField.SUCCEEDED