import os

from http.server import BaseHTTPRequestHandler

from response.coredumpHandler import DumpHandler
from response.staticHandler import StaticHandler
from response.badRequestHandler import BadRequestHandler

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        split_path = os.path.splitext(self.path)
        request_extension = split_path[1]

        if request_extension == ".py":
            handler = BadRequestHandler()
        elif self.path.startswith("/core"):
            handler = DumpHandler("coredumps")
            handler.find(self.path[len("/core"):])
        else:
            handler = StaticHandler("public")
            handler.find(self.path)
 
        self.respond({
            'handler': handler
        })
            
    def do_POST(self):
        handler = BadRequestHandler()

        self.respond({
            'handler': handler
        })
        
    def handle_http(self, handler):
        status_code = 404
        try:
            content = handler.getContents()
            status_code = 200
        except:
            content = "404 Not Found"
        
        self.send_response(status_code)
        if status_code == 200:
            self.send_header('Content-type', handler.getContentType())
        else:
            content = "404 Not Found"
        self.end_headers()

        if isinstance( content, (bytes, bytearray) ):
            return content

        return bytes(content, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['handler'])
        self.wfile.write(response)