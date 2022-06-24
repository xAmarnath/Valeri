from modules._helpers import __load_modules
from modules._config import TOKEN, bot

bot.start(bot_token=TOKEN)

__load_modules()

bot.run_until_disconnected()
