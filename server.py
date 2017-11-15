from http.server import BaseHTTPRequestHandler, HTTPServer


# HTTPRequestHandler class
class Server_Request_Handler(BaseHTTPRequestHandler):
    #HEAD
    def do_HEAD(self):
        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    #GET
    def do_GET(self):
        # Send response to status code
        self.send_response(200)

        print(self.path)



        if self.path == '/start/':
            """start the simulation"""
            self.send_header('Location', '/start')
            self.end_headers()
        else:
            #Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'r') as myfile:
                data = myfile.read().replace('\n', '')
            # Write content as utf-8 data
            self.wfile.write(bytes(data, 'utf-8'))

        return
