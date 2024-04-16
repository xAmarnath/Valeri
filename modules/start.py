from telethon import Button

from ._handler import new_cmd


@new_cmd(pattern="start")
async def _start(msg):
    if not msg.is_private:
        return await msg.reply("Hi, I'm alive ~>_<~")
    buttons = [
        [Button.inline("Commands", data="commands")],
        [
            Button.inline("About", data="about"),
            Button.url("Support", "https://t.me/rosexchat"),
        ],
        [Button.url("Source", "https://github.com/amarnathcjd/valeri")],
    ]
    caption = """
    Hi <b><a href="tg://user?id={}">{}</a></b>, I'm Valeri.
    I'm a bot that can help you with some stuff.
    check out my <code>/help</code> section to see what I can do for you."""
    await msg.reply(
        caption.format(msg.sender_id, msg.sender.first_name),
        parse_mode="html",
        buttons=buttons,
    )


@new_cmd(pattern="help")
async def _help(msg):
    await msg.reply("""Help is on the way!""")
