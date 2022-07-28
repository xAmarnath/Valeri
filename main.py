from modules._config import OWNER_ID, TOKEN, bot
from modules._helpers import load_modules

bot.start(bot_token=TOKEN)

load_modules()

bot.run_until_disconnected()
