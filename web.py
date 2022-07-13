import http.server
import socketserver
from os import getenv

PORT = int(getenv("PORT", "8080"))
Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()