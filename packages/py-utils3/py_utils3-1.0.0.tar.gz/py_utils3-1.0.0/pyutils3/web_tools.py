# pyutils3/web_tools.py
import http.server
import socketserver
import os

class App:
    def __init__(self, host="127.0.0.1", port=8080):
        self.routes = {}
        self.host = host
        self.port = port
    
    def route(self, path):
        """ Define a route for the application. """
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator
    
    def get_html_file(self, filename="index.html"):
        """ Serve the HTML file. """
        if os.path.exists(filename):
            return open(filename, "rb").read()
        return b"File Not Found"
    
    def run(self):
        """ Start the HTTP server. """
        handler = self.create_request_handler()
        httpd = socketserver.TCPServer((self.host, self.port), handler)
        print(f"Server started at http://{self.host}:{self.port}")
        httpd.serve_forever()
    
    def create_request_handler(self):
        """ Create a request handler that serves the routes. """
        class RequestHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                path = self.path.strip("/")
                if path in app.routes:
                    content = app.routes[path]()
                else:
                    content = app.get_html_file()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(content)

        return RequestHandler

# Create the app instance
app = App()  # Default host and port
