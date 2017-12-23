from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from validate import validate_bounds


# HTTPRequestHandler class
class Server_Request_Handler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        # print(self.path)

        self.send_response(200)

        if self.path.endswith('.js'):
            # send local js, css, and img files
            self.send_header('Content-type', 'text/javascript')
            self.end_headers()
            self.wfile.write(bytes(open(self.path[1:]).read(), 'utf-8'))
        elif self.path.endswith('.css'):
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            self.wfile.write(bytes(open(self.path[1:]).read(), 'utf-8'))
        elif self.path.endswith('.png'):
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            self.wfile.write(open(self.path[1:], 'rb').read())

        elif self.path == '/start':
            #when the user clicks a button
            """run the simulation"""



        elif "/newcomp?" in self.path:
            """a new component is created"""
            json_data = json.loads(self.path.replace("%22", "\"").split("?")[1])

            # print(json_data)
            #handle circuit updating & validating


        elif "/newwire?" in self.path:
            """create a new wire"""
            wire_data = json.loads(self.path.replace("%22", "\"").split("?")[1])



            # self.send_home()
        elif "/update?" in self.path:
            """a component's properties are updated"""
            update_data = json.loads(self.path.replace("%22", "\"").split("?")[1])

            print(update_data)


        elif "/comp?" in self.path:
            """access the data of an existing component"""
            # will take the place of /update?

        else:
            #Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            index = open('index.html')
            self.wfile.write(bytes(index.read(), 'utf-8'))

        return

    def send_json_response(self, data):
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(data), 'utf-8'))


def run():
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
    print("Server shutting down...")




"""TEMPORARY"""
run()
