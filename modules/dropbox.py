import io
import os
import re
import time

from requests import post
from telethon import Button, events

from ._config import DROP_KEY, bot
from ._handler import newMsg
from ._helpers import human_readable_size

filedb = {}
work_dir = os.getcwd()
file_path = os.path.join(work_dir, "modules/eval.py")


def upload_file(file_path, file_name):
    url = "https://content.dropboxapi.com/2/files/upload"
    headers = {
        "Authorization": "Bearer {}".format(DROP_KEY),
        "Content-Type": "application/octet-stream",
        "Dropbox-API-Arg": '{"path":"/uploads/'
        + file_name
        + '","mode":{".tag":"overwrite"}}',
    }
    try:
        with open(file_path, "rb") as f:
            r = post(url, headers=headers, data=f)
    except OSError:
        return {"error": "File not found"}
    return r.json()


def get_download_url(file_name):
    url = "https://api.dropboxapi.com/2/sharing/create_shared_link_with_settings"
    headers = {
        "Authorization": "Bearer {}".format(DROP_KEY),
    }
    data = {
        "path": "/uploads/" + file_name,
    }
    try:
        r = post(url, headers=headers, json=data)
    except OSError:
        return {"error": "File not found"}
    r = r.json()
    if r.get("error_summary") and "shared_link_already_exists" in str(
        r.get("error_summary")
    ):
        url = "https://api.dropboxapi.com/2/sharing/list_shared_links"
        r = post(url, headers=headers, json=data)
        r = r.json()
        return r["links"][0]["url"], r["links"][0]["size"]
    return r["url"], r["size"]


def list_folder(path, format=True):
    url = "https://api.dropboxapi.com/2/files/list_folder"
    headers = {
        "Authorization": "Bearer {}".format(DROP_KEY),
        "Content-Type": "application/json",
    }
    data = {
        "path": path,
    }
    r = post(url, headers=headers, json=data)
    r = r.json()
    if not format:
        return [i["name"] for i in r["entries"]]
    dolfin_emoji = "\U0001F431"
    files = f"**{dolfin_emoji} Dropbox files**\n"
    for file in r["entries"]:
        if file[".tag"] == "folder":
            files += (
                "📁 "
                + file["name"]
                + " "
                + (human_readable_size(file["size"]) if file.get("size") else "")
                + "\n"
            )
        else:
            files += "📄 {} -{}\n".format(
                file["name"],
                human_readable_size(file["size"]) if file.get("size") else "",
            )
    files += "**📁 Path**: " + path
    return files


def get_space_usage():
    url = "https://api.dropboxapi.com/2/users/get_space_usage"
    headers = {
        "Authorization": "Bearer {}".format(DROP_KEY),
    }
    r = post(url, headers=headers, json=None)
    r = r.json()
    print(r)
    return r["used"], r["allocation"]["allocated"]


def delete_file(file_name):
    url = "https://api.dropboxapi.com/2/files/delete_v2"
    headers = {
        "Authorization": "Bearer {}".format(DROP_KEY),
        "Content-Type": "application/json",
    }
    data = {
        "path": "/uploads/" + file_name,
    }
    r = post(url, headers=headers, json=data)
    r = r.json()
    return r


def search_file(file_name):
    url = "https://api.dropboxapi.com/2/files/search_v2"
    headers = {
        "Authorization": "Bearer {}".format(DROP_KEY),
        "Content-Type": "application/json",
    }
    data = {
        "query": file_name,
    }
    r = post(url, headers=headers, json=data)
    r = r.json()
    matches = []
    for match in r["matches"]:
        if match["metadata"]["metadata"].get("name"):
            matches.append(match["metadata"]["metadata"]["name"])
    return matches


@newMsg(
    pattern="(drop|dropbox|upload|space|list|geturl|delfile|filesearch|dropboxhelp)"
)
async def _dropbox(e):
    if not DROP_KEY:
        return await e.reply("Dropbox API key not set.")
    cmd = e.text.split(" ")[0][1:]
    if cmd == "upload" or cmd == "drop":
        startTime = time.time()
        if not e.reply_to_msg_id:
            return await e.reply("Reply to a file to upload.")
        reply = await e.get_reply_message()
        if not reply.media:
            return await e.reply("Reply to a file to upload.")
        file = await e.client.download_media(reply)
        if len(e.text.split(" ")) > 1:
            file_name = e.text.split(" ")[1]
        else:
            file_name = file.split("/")[-1]
        r = upload_file(file, file_name)
        if r.get("error"):
            return await e.reply(r["error_summary"])
        url, _ = get_download_url(file_name)
        os.remove(file)
        endTime = time.time()
        dropbox = (
            f"**Dropbox upload complete in {endTime - startTime:.2f} seconds.**\n"
            f"**Name**: {file_name}\n"
            f"**Size:** {human_readable_size(r['size'])} \n"
            f"**File ID:** {r['id']} \n"
            f"**Path:** {r['path_display']}"
        )
        await e.reply(
            dropbox,
            buttons=[Button.url(text="Download", url=url)],
            parse_mode="markdown",
            link_preview=False,
        )
    elif cmd == "list":
        if len(e.text.split(" ")) > 1:
            path = e.text.split(" ")[1]
        else:
            path = "/uploads/"  # default path
        r = list_folder(path)
        if len(r) > 4096 or "-l" in e.text:
            with io.BytesIO(str.encode(r)) as out_file:
                out_file.name = "list.txt"
                return await e.client.send_file(
                    e.chat_id,
                    out_file,
                    force_document=True,
                    reply_to=e,
                    caption="`List of files in the folder:`",
                )
        await e.reply(r)
    elif cmd == "space":
        used, total = get_space_usage()
        usage_percent = round(used / total * 100, 2)
        USAGE = (
            "**Dropbox Usage:**\n"
            + "**Used:** "
            + human_readable_size(used)
            + "\n"
            + "**Total:** "
            + human_readable_size(total)
            + "\n"
            + "**Usage:** "
            + str(usage_percent)
            + "%"
        )
        return await e.reply(USAGE)
    elif cmd == "geturl":
        if len(e.text.split(" ")) > 1:
            file_name = e.text.split(" ")[1]
        else:
            return await e.reply("Specify file name.")
        dp = await e.reply("getting URL...")
        url, size = get_download_url(file_name)
        dropbox = """**DROPBOX FILE**\n**📁 Path:** /uploads/{path}\n**📄 Name:** {name}\n**📄 Size:** {size}""".format(
            path=file_name, name=file_name, size=human_readable_size(int(size))
        )
        await dp.edit(
            dropbox,
            parse_mode="md",
            link_preview=False,
            buttons=[Button.url("Download \U0001F4E2", url)],
        )
    elif cmd == "delfile":
        if len(e.text.split(" ")) > 1:
            file_name = e.text.split(" ")[1]
        else:
            files = list_folder("/uploads/", False)
            if len(files) == 0:
                return await e.reply("No files in the folder.")
            buttons = []
            btns = []
            column = 0
            for file in files:
                btns.append(
                    Button.inline(file, data="deldp_{}x{}".format(len(buttons), column))
                )
                column += 1
                if column == 3:
                    buttons.append(btns)
                    btns = []
                    column = 0
            if len(btns) > 0:
                buttons.append(btns)
            await e.reply(
                "Choose a file to delete.",
                buttons=buttons,
                parse_mode="markdown",
                link_preview=False,
            )
    elif cmd == "filesearch":
        if len(e.text.split(" ")) > 1:
            file_name = e.text.split(" ")[1]
        else:
            return await e.reply("Specify file name.")
        files = search_file(file_name)
        if len(files) == 0:
            return await e.reply("No files found.")
        buttons = []
        btns = []
        column = 0
        for file in files:
            btns.append(
                Button.inline(file, data="showfile_{}x{}".format(len(buttons), column))
            )
            column += 1
            if column == 3:
                buttons.append(btns)
                btns = []
                column = 0
        if len(btns) > 0:
            buttons.append(btns)
        await e.reply(
            "Search Results", buttons=buttons, parse_mode="markdown", link_preview=False
        )
    elif cmd == "dropboxhelp":
        _help = """**Dropbox Commands:**
        drop|upload <file> - Upload a file to Dropbox
        space - Show your Dropbox usage
        list <path> - List files in a folder
        geturl <file> - Get a URL to download a file
        delfile <file> - Delete a file
        filesearch <file> - Search for a file
        dropboxhelp - Show this help
        """
        await e.reply(_help, parse_mode="markdown", link_preview=False)
    else:
        dropbox_stats = "**Dropbox Connection Active**\n"
        await e.reply(dropbox_stats, parse_mode="markdown", link_preview=False)


@bot.on(events.CallbackQuery(data=re.compile("deldp_(\d+)x(\d+)")))
async def _delfilecq(e):
    row, column = e.data.decode("utf-8").split("_")[1].split("x")
    file_name = (
        (await e.get_message()).reply_markup.rows[int(row)].buttons[int(column)].text
    )
    delete_file(file_name)
    await e.edit("**Deleted file:** `{}`".format(file_name))


@bot.on(events.CallbackQuery(data=re.compile("showfile_(\d+)x(\d+)")))
async def _showfilecq(e):
    row, column = e.data.decode("utf-8").split("_")[1].split("x")
    file_name = (
        (await e.get_message()).reply_markup.rows[int(row)].buttons[int(column)].text
    )
    url, size = get_download_url(file_name)
    dropbox = """**DROPBOX FILE**\n**📁 Path:** /uploads/{path}\n**📄 Name:** {name}\n**📄 Size:** {size}""".format(
        path=file_name, name=file_name, size=human_readable_size(int(size))
    )
    await e.edit(
        dropbox,
        parse_mode="md",
        link_preview=False,
        buttons=[Button.url("Download \U0001F4E2", url)],
    )
