import importlib
import logging
from os import listdir, path

import telethon

from ._config import OWNER_ID, bot


def __load_modules():
    # Load all modules in the modules folder
    for module in listdir(path.dirname(__file__)):
        if module.startswith("_") or not module.endswith(".py"):
            continue
        importlib.import_module("modules." + module[:-3])
        logging.info("Loaded module: %s", module[:-3])


def human_readable_size(size, speed=False):
    # Convert a size in bytes to a human readable string
    variables = ["bytes", "KB", "MB", "GB", "TB"]
    if speed:
        variables = ["bps", "Kbps", "Mbps", "Gbps", "Tbps"]
    for x in variables:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0
    return "%3.1f %s" % (size, "TB")


async def get_user(e: telethon.events.NewMessage.Event):
    user: telethon.tl.types.User
    arg = ""
    args = e.text.split(maxsplit=2)
    if e.is_reply:
        user = (await e.get_reply_message()).sender
        arg = (args[1] + (args[2] if len(args) > 2 else "")) if len(args) > 1 else ""
    else:
        if len(args) == 1:
            await e.reply("No user specified")
            return None, ""
        try:
            user = await e.client.get_entity(args[1])
        except BaseException as ex:
            await e.reply(str(ex))
            return
        arg = args[2] if len(args) > 2 else ""
    return user, arg


def get_mention(user: telethon.tl.types.User, mode: str = "md"):
    # Get a mention of a user
    if mode == "md":
        return "[" + user.first_name + "](tg://user?id=" + str(user.id) + ")"
    elif mode == "html":
        return '<a href="tg://user?id=' + str(user.id) + '">' + user.first_name + "</a>"


async def is_worth(right, chat, user, admin_check=True):
    # Check if a user has a certain right in a chat
    if user == OWNER_ID:
        return True
    try:
        p = await bot(telethon.functions.channels.GetParticipantRequest(chat, user))
    except telethon.errors.rpcerrorlist.UserNotParticipantError:
        return False
    if not p:
        return False
    if not admin_check:
        return True
    p: telethon.tl.types.ChannelParticipant = p.participant
    if isinstance(p, telethon.tl.types.ChannelParticipantCreator):
        return True
    if isinstance(p, telethon.tl.types.ChannelParticipantAdmin):
        if p.admin_rights.to_dict()[right]:
            return True
    return False


def human_readable_time(seconds: int):
    # Convert a time in seconds to a human readable string
    variables = ["s", "m", "h", "d"]
    for x in variables:
        if seconds < 60:
            return "%d %s" % (seconds, x)
        seconds /= 60
    return "%d %s" % (seconds, "d")


def human_currency(amount: int):
    # Convert an amount of money to a human readable string
    variables = ["¢", "¥", "€", "£"]
    for x in variables:
        if amount < 100:
            return "%d %s" % (amount, x)
        amount /= 100
    return "%d %s" % (amount, "£")
