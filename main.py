import http.server
import socketserver
from os import getenv

PORT = int(getenv("PORT", "8080"))
Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)

bot.start(bot_token=TOKEN)

__load_modules()

bot.run_until_disconnected()
