from seedrcc import Login, Seedr
from telethon import Button

from ._handler import newCall, newMsg
from ._helpers import human_readable_size
from .db.seedr_db import get_seedr, update_seedr

cache = {}

@newMsg(pattern="account", func=lambda msg: msg.is_private)
async def _seedr_account(msg):
    user = msg.sender_id
    token = get_seedr(user)
    if token is None:
        await msg.reply(
            "⚠️ You don't have any account logged in.",
            buttons=[Button.inline("Login", data="login")],
        )
    else:
        SEEDR = Seedr(str(token), callbackFunc=lambda token: update_seedr(user, token))
        user = SEEDR.getSettings()
        user_caption = "<b>Seedr Account Connected</b>\n"
        user_caption += (
            "<b>Username:</b> <code>" + user["account"]["username"] + "</code>\n"
        )
        user_caption += "<b>Email:</b> <code>" + user["account"]["email"] + "</code>\n"
        user_caption += "<b>ID:</b> <code>" + user["account"]["user_id"] + "</code>\n"
        if int(user["account"]["premium"]) == 1:
            user_caption += "<b>Premium:</b> Yes\n"
        else:
            user_caption += "<b>Premium:</b> No\n"
        await msg.reply(
            user_caption,
            buttons=[Button.inline("Logout", data="logout")],
            parse_mode="HTML",
        )


@newCall(pattern="login", func=lambda call: call.is_private)
async def _seedr_login(call):
    user = call.sender_id
    if get_seedr(user) is not None:
        await call.answer("⚠️ You already have an account logged in.")
        return
    msg = "🛡️ <b>Please follow the instructions to authorize your account</b>\n\n• Go to https://seedr.cc/devices\n• Login your account if not logged in\n• Paste the following code (Click to copy) \n\n<b>CODE: <code>{}</code></b>\n\n• Click the <b>✅ Done</b> button after completion."
    login = Login()
    code = login.getDeviceCode()
    device_code = code["device_code"]
    await call.edit(
        msg.format(code["user_code"]),
        parse_mode="html",
        buttons=[
            [Button.url("Verification URL", code["verification_url"])],
            [Button.inline("✅ Done", data="done_{}".format(device_code))],
        ],
        link_preview=False,
    )


@newCall(pattern="done_(.*)", func=lambda call: call.is_private)
async def _seedr_done(msg):
    device_code = msg.data.decode("utf-8").split("_")[1]
    user = msg.sender_id
    if device_code is None:
        await msg.reply("⚠️ You don't have any account logged in.")
        return
    login = Login()
    login.authorize(deviceCode=device_code)
    update_seedr(user, login.token)
    await msg.reply("✅ Your account has been logged in.")


async def noAccount(msg, call=False):
    """
    Replys to the user if they don't have an account logged in.
    """
    if call:
        return await msg.answer("⚠️ You don't have any account logged in.", alert=True)
    if not msg.is_private:
        return await msg.reply(
            "⚠️ You don't have any account logged in.",
            buttons=[Button.url("Login", "t.me/missvaleri_bot?start=account")],
        )
    await msg.reply(
        "⚠️ You don't have any account logged in.",
        buttons=[Button.inline("Login", data="login")],
    )


def getUserSeedr(user_id):
    if user_id in cache:
       return cache[user_id]
    token = get_seedr(user_id)
    if token is None:
        return None
    client = Seedr(token, callbackFunc=lambda token: update_seedr(user_id, token))
    cache[user_id] = client
    return client


@newMsg(pattern="addtorrent")
async def _seedr_addtorrent(msg):
    seedr = getUserSeedr(msg.sender_id)
    if seedr is None:
        return await noAccount(msg)
    if msg.is_reply:
        r = await msg.get_reply_message()
        if r.text:
            url = r.text
        elif r.media:
            url = r.caption
    else:
        try:
            url = msg.text.split("addtorrent ")[1]
        except:
            return await msg.reply("⚠️ Please specify a torrent link.")
    if url is None:
        return await msg.reply("⚠️ Please specify a torrent link.")
    add_msg = await msg.reply("⚠️ Adding torrent...")
    add = seedr.addTorrent(magnetLink=url)
    print(add)
    if add["result"] == "not_enough_space_added_to_wishlist":
        return await add_msg.edit(
            "⚠️ Not enough space to add torrent, added to wishlist, SIZE: <code>{}</code>".format(
                add["wt"]["size"]
            ),
            parse_mode="HTML",
        )
    await add_msg.edit(
        "✅ Torrent added.\n<b>Name:</b>  <code>{}</code>".format(add["title"]),
        parse_mode="HTML",
        buttons=None,
    )


@newMsg(pattern="seedrusage")
async def _seedr_usage(msg):
    seedr = getUserSeedr(msg.sender_id)
    if seedr is None:
        return await noAccount(msg)
    usage = seedr.getMemoryBandwidth()
    print(usage)
    usage_caption = "<b>Seedr Usage</b>\n"
    usage_caption += "<b>Bandwidth:</b> <code>{}</code>/<code>{}</code>\n".format(
        human_readable_size(usage["bandwidth_used"]),
        human_readable_size(usage["bandwidth_max"]),
    )
    usage_caption += "<b>Space:</b> <code>{}</code>/<code>{}</code>\n".format(
        human_readable_size(usage["space_used"]),
        human_readable_size(usage["space_max"]),
    )
    await msg.reply(usage_caption, parse_mode="HTML")


@newMsg(pattern="files")
async def _seedr_files(msg):
    seedr = getUserSeedr(msg.sender_id)
    if seedr is None:
        return await noAccount(msg)
    files = seedr.listContents()
    caption = "<b>Seedr Files</b>\n"
    buttons = []
    if files["folders"]:
        for i in files["folders"]:
            caption += f"<b>📂 {i['fullname']}</b>\n\n💾 {human_readable_size(i['size'])}, ⏰ {i['last_update']}"
            caption += f"\n\nFiles: /getFiles_{i['id']}\nLink: /getLink_{i['id']}\nDelete: /delete_{i['id']}\n\n"
            buttons.append([Button.inline(f"🚮 {i['fullname'][:30]}", "delete_{i['id']}")])
        await msg.reply(caption, parse_mode="HTML", buttons=buttons)
    else:
        await msg.reply("⚠️ You don't have any files.")


@newMsg(pattern="getfiles_(.*)")
async def _seedr_getfiles(msg):
    seedr = getUserSeedr(msg.sender_id)
    if seedr is None:
        return await noAccount(msg)
    id = msg.text[10:]
    response = seedr.listContents(folderId=id)
    if "error" not in response:
        if "name" in response:
            text = f"<b>📁 {response['name']}</b>\n\n"
            markup = []
            markup.append(
                [
                    Button.inline("🔗 Download Link", data=f"download_{id}"),
                    Button.inline("🗑 Delete", data=f"delete_{id}"),
                ]
            )
            for folder in response["folders"]:
                text += f"🖿 {folder['name']} <b>[ {human_readable_size(folder['size'])}]</b>\n\n"
                text += f"Files: /getFiles_{folder['id']}\n"
                text += f"Delete: /delete_{folder['id']}\n\n"

            for file in response["files"]:
                text += f"<code>{'🎬' if file['play_video'] == True else '🎵' if file['play_audio'] == True else '📄'} {file['name']}</code> <b>[{human_readable_size(file['size'])}]</b>\n\n"
                text += f"Link /fileLink_{'v' if file['play_video'] == True else 'a' if file['play_audio'] == True else 'u'}{file['folder_file_id']}\n"
                text += f"Delete: /remove_{file['folder_file_id']}\n\n"
            markup.append([Button.inline("Open in media player", data=f"open_{id}")])

            await msg.reply(text, parse_mode="HTML", buttons=markup)

    else:
        await msg.reply(response["error"])


@newMsg(pattern="filelink_(.*)")
async def _seedr_filelink(msg):
    seedr = getUserSeedr(msg.sender_id)
    if seedr is None:
        return await noAccount(msg)
    id = msg.text[10:]
    message = "⚠️ Please wait..."
    new_msg = await msg.reply(message)
    response = seedr.fetchFile(id[1:])
    if "error" not in response:
        encodedUrl = response["url"]
        print(encodedUrl)
        text = f"🖹 <b>{response['name']}</b>\n\n"
        text += f"🔗 <code>{encodedUrl}</code>\n\n<b>🔥via @missValeri_Bot</b>"
        markup = []
        markup.append([Button.url("🔗 Download Link", url=encodedUrl)])
        await new_msg.edit(text, parse_mode="HTML", buttons=markup)
    else:
        await new_msg.edit(response["error"])


@newMsg(pattern="remove_(.*)")
async def _seedr_remove(msg):
    seedr = getUserSeedr(msg.sender_id)
    if seedr is None:
        return await noAccount(msg)
    id = msg.text[8:]
    response = seedr.deleteFile(id)
    print(response)
    if "error" not in response:
        await msg.reply("✅ File removed.")
    else:
        await msg.reply(response["error"])


@newMsg(pattern="delete_(.*)")
async def _seedr_delete(msg):
    seedr = getUserSeedr(msg.sender_id)
    if seedr is None:
        return await noAccount(msg)
    id = msg.text[8:]
    response = seedr.deleteFolder(id)
    if "error" not in response:
        await msg.reply("✅ Folder removed.")
    else:
        await msg.reply(response["error"])


@newCall(pattern="delete_(.*)")
async def _seedr_delete_call(call):
    seedr = getUserSeedr(call.from_user.id)
    if seedr is None:
        return await noAccount(call, True)
    id = call.data.decode("utf-8").split("_", 1)[1]
    response = seedr.deleteFolder(id)
    if "error" not in response:
        await call.edit("✅ Folder removed.")
    else:
        await call.answer(response["error"], alert=True)


@newCall(pattern="remove_(.*)")
async def _seedr_remove_call(call):
    seedr = getUserSeedr(call.from_user.id)
    if seedr is None:
        return await noAccount(call, True)
    id = call.data.decode("utf-8").split("_", 1)[1]
    response = seedr.deleteFile(id)
    if "error" not in response:
        await call.edit("✅ File removed.")
    else:
        await call.answer(response["error"], alert=True)


@newCall(pattern="filelink_(.*)")
async def _seedr_filelink_call(call):
    seedr = getUserSeedr(call.from_user.id)
    if seedr is None:
        return await noAccount(call, True)
    id = call.data.decode("utf-8").split("_", 1)[1]
    response = seedr.fetchFile(id)
    if "error" not in response:
        encodedUrl = response["url"]
        text = f"🖹 <b>{response['name']}</b>\n\n"
        text += f"🔗 <code>{encodedUrl}</code>\n\n<b>🔥via @missValeri_Bot</b>"
        markup = []
        markup.append([Button.url("🔗 Download Link", url=encodedUrl)])
        await call.edit(text, parse_mode="HTML", buttons=markup)
    else:
        await call.answer(response["error"], alert=True)


# balance soon
