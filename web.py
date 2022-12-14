from functools import partial
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import os

PORT = os.getenv("PORT", "8080")

with TCPServer(("", int(PORT)), partial(SimpleHTTPRequestHandler, directory=".")) as httpd:
    httpd.serve_forever()
