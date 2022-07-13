import subprocess
from asyncio import sleep

import aria2p
from requests import get

from ._handler import auth_only, newMsg
from ._helpers import human_readable_size


def subprocess_run(cmd):
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True
    )
    return "started"


def aria_start():
    trackers_list = get(
        "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best.txt"
    ).text.replace("\n\n", ",")
    trackers = f"[{trackers_list}]"
    cmd = f"aria2c --enable-rpc --rpc-listen-all=false --rpc-listen-port=6800 --max-connection-per-server=100 --rpc-max-request-size=1024M --check-certificate=false --follow-torrent=mem --seed-time=600 --min-split-size=10M --follow-torrent=mem --split=10 --bt-tracker={trackers} --daemon=true --allow-overwrite=true"
    subprocess_run(cmd)
    aria2 = aria2p.API(aria2p.Client(host="http://localhost", port=6800, secret=""))
    return aria2


aria2p_client = aria_start()


async def check_metadata(gid):
    try:
        t_file = aria2p_client.get_download(gid)
    except aria2p.client.ClientException:
        return None
    if not t_file.followed_by_ids:
        return None
    new_gid = t_file.followed_by_ids[0]
    return new_gid


async def check_progress_for_dl(gid, message, previous):
    complete = False
    while not complete:
        try:
            t_file = aria2p_client.get_download(gid)
        except:
            return await message.edit("Download cancelled by user ...")
        complete = t_file.is_complete
        is_file = t_file.seeder
        try:
            if t_file.error_message:
                print(str(t_file.error_message))
                await message.edit(str(t_file.error_message))
            if t_file.is_complete:
                return await message.edit(
                    f"**Successfully Downloaded {t_file.name}** \n\n"
                    f"> Size:  `{t_file.total_length_string()}` \n"
                    f"> Path:  `{t_file.name}`"
                )
            if not complete and not t_file.error_message:
                if t_file.progress_string() == "100.00%":
                    return await message.edit(
                        f"**Successfully Downloaded {t_file.name}** \n\n"
                        f"> Size:  `{t_file.total_length_string()}` \n"
                        f"> Path:  `{t_file.name}`"
                    )
                percentage = int(t_file.progress)
                downloaded = percentage * int(t_file.total_length) / 100
                prog_str = f"** Downloading! @ {t_file.progress_string()}**"
                if is_file is None:
                    info_msg = f"**Connections:**  `{t_file.connections}`\n"
                else:
                    info_msg = (
                        f"**Connection:**  `{t_file.connections}` \n"
                        f"**Seeds:**  `{t_file.num_seeders}` \n"
                    )
                msg = (
                    f"`{prog_str}` \n\n"
                    f"**Name:**  `{t_file.name or 'unknown'}` \n"
                    f"**Completed:**  `{human_readable_size(downloaded)}` \n"
                    f"**Total:**  `{t_file.total_length_string()}` \n"
                    f"**Speed:**  `{t_file.download_speed_string()}` \n"
                    f"{info_msg}"
                    f"**ETA:**  `{t_file.eta_string()}` \n"
                    f"**GID:**  `{gid}`"
                )
                if msg != previous:
                    await message.edit(msg)
                    previous = msg
            else:
                print("lada")
            await sleep(5)
        except Exception as e:
            if "not found" in str(e) or "'file'" in str(e):
                if "Your Torrent/Link is Dead." not in message.text:
                    await message.edit(f"**Download Canceled,** \n`{t_file.name}`")
            elif "depth exceeded" in str(e):
                t_file.remove(force=True)
                await message.edit(
                    f"**Download Auto Canceled :**\n`{t_file.name}`\nYour Torrent/Link is Dead."
                )


@newMsg(pattern="ariadl")
@auth_only
async def t_url_download(message):
    is_url, is_mag = False, False
    reply = await message.get_reply_message()
    args = message.pattern_match.group(1)
    message = await message.reply("...")
    if reply and reply.document and reply.file.ext == ".torrent":
        tor = await message.client.download_media(reply)
        try:
            download = aria2p_client.add_torrent(
                tor, uris=None, options=None, position=None
            )
        except Exception as e:
            return await message.edit(f"**ERROR:**  `{e}`")
    elif args:
        if args.lower().startswith("http"):
            try:
                is_url = True
                download = aria2p_client.add_uris([args], options=None)
            except Exception as e:
                return await message.edit(f"**ERROR while adding URI** \n`{e}`")
        elif args.lower().startswith("magnet:"):
            is_mag = True
            try:
                download = aria2p_client.add_magnet(args, options=None)
            except Exception as e:
                return await message.edit(f"**ERROR while adding URI** \n`{e}`")
    else:
        return await message.edit("`No torrent given`")
    gid = download.gid
    await message.edit("`Processing......`")
    await check_progress_for_dl(gid=gid, message=message, previous="")
    if is_url:
        file = aria2p_client.get_download(gid)
        if file.followed_by_ids:
            new_gid = await check_metadata(gid)
            await check_progress_for_dl(gid=new_gid, message=message, previous="")
    elif is_mag:
        await sleep(4)
        new_gid = await check_metadata(gid)
        await check_progress_for_dl(gid=new_gid, message=message, previous="")


@newMsg(pattern="ariadelall")
@auth_only
async def clr_aria(message):
    removed = False
    try:
        removed = aria2p_client.remove_all(force=True)
        aria2p_client.purge()
    except Exception as e:
        print(e)
    await sleep(1)
    if not removed:
        subprocess_run("aria2p remove-all")
    await message.reply("`Successfully cleared all downloads.`")


@newMsg(pattern="cancel")
async def remove_a_download(message):
    g_id = message.pattern_match.group(1)
    try:
        downloads = aria2p_client.get_download(g_id)
    except:
        await message.reply("GID not found ....")
        return
    file_name = downloads.name
    await message.reply(f"**Successfully cancelled download.** \n`{file_name}`")
    aria2p_client.remove(downloads=[downloads], force=True, files=True, clean=True)


@newMsg(pattern="ariastatus$")
async def show_all(message):
    downloads = aria2p_client.get_downloads()
    msg = "**On Going Downloads**\n\n"
    for download in downloads:
        if str(download.status) != "complete":
            msg = (
                msg
                + "**File:**  ```"
                + str(download.name)
                + "```\n**Speed:**  "
                + str(download.download_speed_string())
                + "\n**Progress:**  "
                + str(download.progress_string())
                + "\n**Total Size:**  "
                + str(download.total_length_string())
                + "\n**Status:**  "
                + str(download.status)
                + "\n**ETA:**  "
                + str(download.eta_string())
                + "\n**GID:**  "
                + f"`{str(download.gid)}`"
                + "\n\n"
            )
    await message.reply(msg)


@newMsg(pattern="ariapause")
async def pause_all(message):
    await message.reply("`Pausing downloads...`")
    aria2p_client.pause_all()


@newMsg(pattern="ariaresume")
async def resume_all(message):
    await message.reply("`Resuming downloads...`")
    aria2p_client.resume_all()
