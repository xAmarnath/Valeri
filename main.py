from modules._config import TOKEN, bot
from modules._helpers import __load_modules
import http.server
import socketserver
from os import getenv

PORT = getenv("PORT", 8080)
Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)

bot.start(bot_token=TOKEN)

__load_modules()

bot.run_until_disconnected()
