import telethon

from ._handler import newMsg
from ._helpers import get_mention, get_user, has_admin_rights
from .db.warns_db import get_warn_count, get_warn_setting, remove_all_warns, warn_user


@newMsg(pattern="warn")
async def warn(e):
    if not e.is_group:
        await e.reply("`Warns can only be used in groups!`")
        return
    has_right, msg = await has_admin_rights(e.chat_id, e.sender_id, "ban_users")
    if not has_right:
        return await e.reply(msg)
    user, args = await get_user(e)
    if user is None:
        return await e.reply("`Couldn't find user!`")
    if user.id == e.sender_id:
        return await e.reply("`You can't warn yourself!`")
    user: telethon.tl.types.User
    if user.is_self:
        return await e.reply("What are you trying to do? You can't warn me!")
    if user.bot:
        return await e.reply("You can't warn bots!")
    warn_count = get_warn_count(user.id, e.chat_id)
    warn_settings = get_warn_setting(e.chat_id)
    reason = "<b>Reason:</b> {}".format(args) if args else ""
    if warn_count + 1 < warn_settings["max_warnings"]:
        await e.reply(
            "<b>{}</b> has {}/{} warnings, be careful!{}".format(
                get_mention(user), warn_count, warn_settings["max_warnings"], reason
            )
        )
        warn_user(user.id, e.chat_id, args, e.sender_id)
    else:
        print("oki")
        remove_all_warns(user.id, e.chat_id)
