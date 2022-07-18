from telethon import TelegramClient as client

from ._config import API_HASH, API_KEY
from ._handlers import newMsg
from ._helpers import get_text_content

clients = []


async def start_(msg):
    return await msg.reply("Hello Im, botID-{}")


def load_handlers(bot):
    bot.add_event_handler(start_, events.NewMessage(pattern="^[!/?]start$"))


async def addBot(token):
    botID = token.split(":")[0]
    tgClient = client(botID + "-0", API_KEY, API_HASH)
    clients.append(tgClient)
    try:
        await tgClient.start(bot_token=token)
    except Exception as d:
        return str(d)
    load_handlers(tgClient)
    return ""


@newMsg(pattern="addbot")
async def addbt(e):
    tok = await get_text_content(e)
    add = await addBot(tok)
    if add != "":
        return await e.reply(add)
    return await e.reply("Sucessfully added bot.")
