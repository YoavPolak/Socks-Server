from enum import IntEnum

class AddressType(IntEnum):
    """
    Supported address types of the server.
    """
    IPV4 = 1
    DOMAIN = 3
    IPV6 = 4