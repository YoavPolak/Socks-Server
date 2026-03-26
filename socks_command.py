from enum import IntEnum

class SocksCommand(IntEnum):
    """
    Socks supported commands by the server.
    """
    CONNECT = 1
    # BIND: 2
    # UDP_ASSOCIATE: 3
