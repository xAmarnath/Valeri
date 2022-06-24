from telethon import events
from ._config import bot
from ._helpers import IsWorth


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

def adminsOnly(rights=None):
    def decorator(func):
        async def wrapper(event):
            if event.is_private:
                return await func(event)
            if not IsWorth(event.chat_id):
                return
            return await func(event)
       
