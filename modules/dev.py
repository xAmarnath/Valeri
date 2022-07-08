from os import listdir, path

from ._handler import auth_only, master_only, newMsg
from ._helpers import get_mention, get_text_content, get_user, human_readable_size
from ._transfers import fast_upload
from .db.auth import add_auth, get_auth, is_auth, remove_auth


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
        )
    except OSError:
        await e.reply("`Failed to upload.`")
        return


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
            "<b>{}</b> is already authorized.".format(get_mention(user)),
            parse_mode="html",
        )
        return
    add_auth(user.id)
    await e.reply(
        "<b>{}</b> is now authorized.".format(get_mention(user)), parse_mode="html"
    )


@newMsg(pattern="(unauth|rmauth)")
@master_only
async def _unauth(e):
    user, arg = await get_user(e)
    if user is None:
        return await e.reply("Specify a user to unauthorize.")
    if not is_auth(user.id):
        await e.reply(
            "<b>{}</b> is not authorized.".format(get_mention(user)), parse_mode="html"
        )
        return
    remove_auth(user.id)
    await e.reply(
        "<b>{}</b> is now unauthorized.".format(get_mention(user)), parse_mode="html"
    )
