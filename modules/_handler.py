from functools import wraps

from telethon import events

from ._config import OWNER_ID, bot
from ._helpers import is_worth
from .db.auth import is_auth
from .db.stats_db import add_user, already_added_user


def newMsg(**args):
    """
    Decorator for handling new messages.
    """
    args["pattern"] = "(?i)^[!/-]" + args["pattern"] + "(?: |$|@MissValeri_Bot)(.*)"

    def decorator(func):
        async def wrapper(event):
            await func(event)
            if not already_added_user(event.sender_id):
                add_user(event.sender_id)

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
        if not is_worth(right, event.chat_id, event.sender_id):
            return
        return await func(event)


def master_only(func):
    """
    Decorator for handling messages from the master.
    """

    @wraps(func)
    async def sed(event):
        if event.sender_id == OWNER_ID:
            await func(event)
        else:
            await event.reply("You are not authorized to use this command")

    return sed


def auth_only(func):
    """
    Decorator for handling messages from authenticated users.
    """

    @wraps(func)
    async def sed(event):
        if any([is_auth(event.sender_id), event.sender_id == OWNER_ID]):
            await func(event)
        return

    return sed


def newCall(**args):
    """
    Decorator for handling new calls.
    """

    def decorator(func):
        async def wrapper(event):
            await func(event)

        bot.add_event_handler(wrapper, events.CallbackQuery(**args))
        return func

    return decorator


def newIn(**args):
    """
    Decorator for handling new inline queries.
    """

    def decorator(func):
        async def wrapper(event):
            await func(event)

        bot.add_event_handler(wrapper, events.InlineQuery(**args))
        return func

    return decorator


RED_LIST = {}


def is_user_spam(user_id) -> bool:
    if not user_id in RED_LIST:
        RED_LIST[user_id] = []
