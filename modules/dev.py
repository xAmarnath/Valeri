import re
import sys
from os import environ, execle, listdir, path, remove, system

import speedtest
import tinytag
from telethon import types

from ._handler import auth_only, master_only, newMsg
from ._helpers import (
    generate_thumbnail,
    get_mention,
    get_text_content,
    get_user,
    get_video_metadata,
    human_readable_size,
)
from ._transfers import upload_file
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
        directory = directory + "/" if not directory.endswith("/") else directory
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
            if file.lower().endswith((".mp4", ".mkv", ".webm", ".3gp", ".mpeg")):
                emoji = "🎥"
            elif file.lower().endswith((".mp3", ".wav", ".flv", ".ogg", ".opus")):
                emoji = "🎵"
            elif file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                emoji = "🖼"
            elif file.lower().endswith(".gif"):
                emoji = "🎇"
            elif file.lower().endswith((".zip", ".rar", ".7z", ".tar", ".gzip")):
                emoji = "🗜"
            elif file.lower().endswith(
                (".json", ".xml", ".txt", ".text", ".csv", ".pptx", ".md")
            ):
                emoji = "📝"
            elif file.lower().endswith(".py"):
                emoji = "🐍"
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
    msg = await e.reply("`Uploading...`")
    caption = ""
    thumb, attributes, streamable, chat, action = (
        None,
        [],
        False,
        e.chat_id,
        "document",
    )
    if any([re.search(x, l.lower()) for x in ["--chat", "-c"]]):
        if "--chat" in l.lower():
            args = l.split("--chat")
            l = re.sub("--chat (.*) -", "-", l).strip()
            if "--chat" in l.lower():
                l = re.sub("--chat (.*)", "", l).strip()
        else:
            args = l.split("-c")
            l = re.sub("-c (.*) -", "-", l).strip()
            if "-c" in l.lower():
                l = re.sub("-c (.*)", "", l).strip()
        chat = args[1].split("-")[0].strip() if len(args) > 1 else e.chat_id
        chat = int(chat) if str(chat).isdigit() else chat
    if any([re.search(x, l.lower()) for x in ["--text", "-t"]]):
        args = l.split("--text") if "--text" in l else l.split("-t")
        caption = args[1] if len(args) > 1 else ""
        l = args[0].strip()
    filename = l.split("\\")[-1]
    caption = caption or filename
    filename = filename.split("/")[-1] if filename == l else filename
    if l.endswith(("mp4", "mkv", "3gp", "webm")):
        thumb = generate_thumbnail(l, l + "_thumb.jpg")
        d, w, h = get_video_metadata(l)
        attributes = [
            types.DocumentAttributeVideo(w=w, h=h, duration=d, supports_streaming=True)
        ]
        streamable = True
        action = "video"
    elif l.endswith(("mp3", "wav", "flv", "ogg", "opus")):
        metadata = tinytag.TinyTag.get(l)
        attributes = [
            types.DocumentAttributeAudio(
                duration=int(metadata.duration or "0"),
                performer=metadata.artist or "Me",
                title=metadata.title or "Unknown",
            )
        ]
        action = "audio"
    try:
        file = await upload_file(e.client, l)
        async with e.client.action(chat, action):
            await e.client.send_message(
                chat,
                caption,
                file=file,
                thumb=thumb,
                attributes=attributes,
                supports_streaming=streamable,
            )
        await msg.delete()
        if thumb:
            remove(thumb)
    except Exception as exc:
        await msg.edit("`error on uploading.\n{}`".format(str(exc)))


@newMsg(pattern="dl")
@auth_only
async def _dl(e):
    r = await e.get_reply_message()
    if not r:
        return await e.reply("`Reply to a file.`")
    if not r.media:
        return await e.reply("`Reply to a file.`")
    msg = await e.reply("`Downloading...`")
    await e.client.download_media(r.media, "./")
    await msg.edit("`Downloaded successfully.`")


@newMsg(pattern="auth")
@master_only
async def _auth(e):
    if not e.reply_to and not len(e.text.split(None)) > 1:
        AUTH_LIST = "Auth list:\n"
        sno = 0
        for user in get_auth():
            sno += 1
            AUTH_LIST += (
                "<b>{sno}.</b> <a href='tg://user?id={user}'>{user_name}</a>\n".format(
                    sno=sno, user=user, user_name=user
                )
            )
        await e.reply(AUTH_LIST, parse_mode="HTML")
        return
    user, _ = await get_user(e)
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
    user, _ = await get_user(e)
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
