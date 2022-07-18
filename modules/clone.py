from telethon import TelegramClient as client
from telethon import events

from ._config import API_HASH, API_KEY
from ._handler import auth_only, newMsg
from ._helpers import get_text_content

clients = []


async def start_(msg):
    me = await msg.client.get_me()
    return await msg.reply(f"Hello Im, @-{me.username}, running in cloneMode.")


def load_handlers(bot):
    bot.add_event_handler(start_, events.NewMessage(pattern="^[!/?]start$"))


async def addBot(token):
    botID = token.split(":")[0]
    tgClient = client(botID + "-0", API_KEY, API_HASH)
    clients.append(tgClient)
    try:
        await tgClient.start(bot_token=token)
    except Exception as err:
        return str(err)
    load_handlers(tgClient)
    return ""


@newMsg(pattern="addbot")
@auth_only
async def addbt(e):
    tok = await get_text_content(e)
    if not tok:
        return await e.reply("No token given.")
    add = await addBot(tok)
    if add != "":
        return await e.reply(add)
    return await e.reply("Sucessfully added bot.")
