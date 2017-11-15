from server import *


if __name__ == '__main__':
    print('Starting server...')

    # Server settings
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, Server_Request_Handler)

    #server keeps running indefinitely until interrupted by ctrl+c
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('\n')
