from functools import wraps

from telethon import events

from ._config import bot
from ._helpers import IsWorth
from .db.auth import isAUTH


def newMsg(**args):
    args["pattern"] = "(?i)^[!/]" + args["pattern"] + "(?: |$|@MissValeri_Bot)(.*)"

    def decorator(func):
        async def wrapper(event):
            try:
                await func(event)
            except Exception as e:
                await event.reply(str(e))

        bot.add_event_handler(wrapper, events.NewMessage(**args))
        return func

    return decorator


def adminsOnly(func, right=""):
    @wraps(func)
    async def sed(event):
        if event.is_private:
            return await func(event)
        if not IsWorth(right, event.chat_id, event.sender_id):
            return
        return await func(event)


def authOnly(func):
    @wraps(func)
    async def sed(event):
        if event.sender_id:
            if isAUTH(event.sender_id):
                return await func(event)
        return await event.reply("You are not authorized to use this command.")
