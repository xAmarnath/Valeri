from modules._config import TOKEN, bot
from modules._helpers import load_modules
from modules.ktu import fetch_and_check_results

bot.start(bot_token=TOKEN)

load_modules()

import asyncio
asyncio.ensure_future(fetch_and_check_results())

bot.run_until_disconnected()