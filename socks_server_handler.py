from socketserver import BaseRequestHandler, TCPServer, ThreadingMixIn
from proxy_handler import ProxyHandler
from address_reader import AddressReader
from authentication_handler import AuthenticationHandler
from request_handler import RequestHandler
from response_serializer import ResponseSerializer
from socks_connection import SocksConnection
from connection_state import ConnectionState
from socks_parser import SocksParser

class SocksServerHandler(BaseRequestHandler):

    def handle(self):
        """
        """
        socks_parser = SocksParser()
        address_reader = AddressReader()
        response_serializer = ResponseSerializer()
        authentication_handler = AuthenticationHandler(socks_parser)
        request_handler = RequestHandler(socks_parser, address_reader, response_serializer)
        proxy_handler = ProxyHandler()

        socks_connection = SocksConnection(self.request, ConnectionState.AUTHENTICATION, authentication_handler, request_handler, proxy_handler)
        socks_connection.handle()

class SocksServer(ThreadingMixIn, TCPServer):
    # allow_reuse_address = True
    pass