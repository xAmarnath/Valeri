import re
import sys
from os import environ, execle, listdir, path, system

import speedtest

from ._handler import auth_only, master_only, newMsg
from ._helpers import get_mention, get_text_content, get_user, human_readable_size
from ._transfers import fast_download, fast_upload
from .db.auth import add_auth, get_auth, is_auth, remove_auth


def is_bl(code):
    if any([re.search(x, code.lower()) for x in ["net", "bat", "chmod"]]):
        return True
    return False


@newMsg(pattern="ls")
@auth_only
async def _ls(e):
    try:
        directory = e.text.split(" ", 1)[1]
    except IndexError:
        directory = "./"
    contents = listdir(directory)
    if len(contents) == 0:
        await e.reply("`No files found.`")
        return
    caption = "<b>Files in <code>{}</code>:</b>\n".format(directory)
    folder_count = 0
    file_count = 0
    for file in contents:
        size = path.getsize(directory + file)
        if path.isdir(directory + file):
            folder_count += 1
            caption += "📁 <code>{}</code> (<code>{}</code>)\n".format(
                file, human_readable_size(size)
            )
        else:
            file_count += 1
            if file.endswith(".mp4") or file.endswith(".mkv") or file.endswith(".webm"):
                emoji = "🎥"
            elif file.endswith(".mp3") or file.endswith(".wav"):
                emoji = "🎵"
            elif (
                file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png")
            ):
                emoji = "🖼"
            elif file.endswith(".gif"):
                emoji = "🎇"
            elif file.endswith(".zip") or file.endswith(".rar") or file.endswith(".7z"):
                emoji = "🗜"
            else:
                emoji = "📄"
            caption += "{} <code>{}</code> (<code>{}</code>)\n".format(
                emoji, file, human_readable_size(size)
            )
    caption += "\n<b>{} folders, {} files</b>".format(folder_count, file_count)
    await e.reply(caption, parse_mode="html")


@newMsg(pattern="ul")
@auth_only
async def _ul(e):
    l = await get_text_content(e)
    if not l:
        return await _ls(e)
    try:
        await fast_upload(
            e.client,
            l,
            reply=await e.reply("`Uploading...`"),
        )
    except OSError:
        await e.reply("`Failed to upload.`")
        return


@newMsg(pattern="dl")
@auth_only
async def _dl(e):
    r = await e.get_reply_message()
    if not r:
        return await e.reply("`Reply to a file.`")
    if not r.media:
        return await e.reply("`Reply to a file.`")
    await fast_download(e.client, r, reply=await e.reply("`Downloading...`"))


@newMsg(pattern="auth")
@master_only
async def _auth(e):
    if not e.reply_to and not len(e.text.split(None)) > 1:
        AUTH_LIST = "Auth list:\n"
        sno = 0
        for user in get_auth():
            sno += 1
            AUTH_LIST += "<b>{}.</b> <a href='tg://user?id={}'>{}</a>\n".format(
                sno, user, user
            )
        await e.reply(AUTH_LIST, parse_mode="HTML")
        return
    user, arg = await get_user(e)
    if is_auth(user.id):
        await e.reply(
            "<b>{}</b> is already authorized.".format(get_mention(user, "html")),
            parse_mode="html",
        )
        return
    add_auth(user.id)
    await e.reply(
        "<b>{}</b> is now authorized.".format(get_mention(user, "html")),
        parse_mode="html",
    )


@newMsg(pattern="(unauth|rmauth)")
@master_only
async def _unauth(e):
    user, arg = await get_user(e)
    if user is None:
        return await e.reply("Specify a user to unauthorize.")
    if not is_auth(user.id):
        await e.reply(
            "<b>{}</b> is not authorized.".format(get_mention(user, "html")),
            parse_mode="html",
        )
        return
    remove_auth(user.id)
    await e.reply(
        "<b>{}</b> is now unauthorized.".format(get_mention(user, "html")),
        parse_mode="html",
    )


@newMsg(pattern="update")
@master_only
async def update_origin(e):
    msg = await e.reply("`Updating...`")
    system("git pull")
    await msg.edit("`Restarting...`")
    args = [sys.executable, "main.py"]
    execle(sys.executable, *args, environ)


@newMsg(pattern="restart")
@master_only
async def restart_process(e):
    await e.reply("`Restarting...`")
    args = [sys.executable, "main.py"]
    execle(sys.executable, *args, environ)


@newMsg(pattern="speedtest")
@auth_only
async def _speedtest(e):
    msg = await e.reply("Testing internet speed...")
    st = speedtest.Speedtest()
    download = st.download()
    upload = st.upload()
    ping = st.results.ping
    server = st.results.server.get("name", "Unknown")
    isp = st.results.client.get("isp", "Unknown")
    ip = st.results.client.get("ip", "Unknown")
    country = st.results.client.get("country", "Unknown")
    result = (
        f"**Speedtest Results:**\n\n"
        f"**Download:** `{human_readable_size(download, True)}`\n"
        f"**Upload:** `{human_readable_size(upload, True)}`\n"
        f"**Ping:** `{ping} ms`\n"
        f"**Server:** `{server}`\n"
        f"**ISP:** `{isp}`\n"
        f"**IP:** `{ip}`\n"
        f"**Country:** `{country}`"
    )
    await msg.edit(result)
