from enum import StrEnum

class ConnectionState(StrEnum):
    """
    Client connection states.
    """
    AUTHENTICATION = "AUTHENTICATION"
    REQUEST = "REQUEST"
    PROXY = "PROXY"
    CLOSED = "CLOSED"