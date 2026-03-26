from reply_field import ReplyField


class InvalidSocksRequest(Exception):
    """
    Thrown when invalid socks request is sent. The exception
    when it can be described by reply field status codes.
    """
    def __init__(self, message: str, reply: ReplyField | None = None):
        super().__init__(message)
        self.reply: ReplyField = reply