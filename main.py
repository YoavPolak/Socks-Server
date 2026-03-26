from socks_server_handler import SocksServerHandler, SocksServer

def main():
    HOST, PORT = "localhost", 1080

    server = SocksServer((HOST, PORT), SocksServerHandler)
    with server:
        server.serve_forever()
if __name__ == "__main__":
    main()