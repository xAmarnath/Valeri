from functools import wraps

from telethon import events

from ._config import bot
from .db.auth import is_auth


def newMsg(**args):
    """
    Decorator for handling new messages.
    """
    args["pattern"] = "(?i)^[!/]" + args["pattern"] + "(?: |$|@MissValeri_Bot)(.*)"

    def decorator(func):
        async def wrapper(event):
            try:
                await func(event)
            except Exception as e:
                await event.reply("Error: {}\n**{}**".format(str(e), str(type(e))))

        bot.add_event_handler(wrapper, events.NewMessage(**args))
        return func

    return decorator


def adminsOnly(func, right=""):
    """
    Decorator for handling messages from admins.
    """

    @wraps(func)
    async def sed(event):
        if event.is_private:
            return await func(event)
        if not IsWorth(right, event.chat_id, event.sender_id):
            return
        return await func(event)


def authOnly(func):
    """
    Decorator for handling messages from authorized users.
    """

    @wraps(func)
    async def sed(event):
        if event.is_private:
            return await func(event)
        if not is_auth(event.sender_id):
            return
        return await func(event)

    @wraps(func)
    async def sed(event):
        if event.sender_id:
            if is_auth(event.sender_id):
                return await func(event)
        return await event.reply("You are not authorized to use this command.")
