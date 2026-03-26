from enum import IntEnum

class ReplyField(IntEnum):
    """
    Implemented reply field by socks server.
    """
    SUCCEEDED = 0
    SERVER_FAILURE = 1
    CONNECTION_NOT_ALLOWED = 2
    NETWORK_UNREACHABLE = 3
    HOST_UNREACHABLE = 4
    CONNECTION_REFUSED = 5
    TTL_EXPIRED = 6
    COMMAND_NOT_SUPPORTED = 7
    ATYP_NOT_SUPPORTED = 8
    INVALID_SOCKS_VERSION = 9
    UNKNOWN_ERROR = 10
    # o  X'09' to X'FF' unassigned