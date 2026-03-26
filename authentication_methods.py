from enum import Enum

class AuthenticationMethods(Enum):
    """
    Authentication supported methods by the server.
    """
    NO_AUTHENTICATION = 0
    NO_ACCEPTABLE_METHODS = 255