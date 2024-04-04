import requests

from ._handler import new_cmd


@new_cmd(pattern="(telegraph|tg) ?(.*)")
async def telegraph(e):
    await e.reply("To Be Implemeneted.")


@new_cmd(pattern="(cupload|cup) ?(.*)")
async def c_upload(e):
    if not e.is_Reply:
        return await e.edit("Reply to a media to upload it to Cloud.")
    msg = await e.reply("Processing...")
    reply_ = await e.get_reply_message()
    if not reply_.media:
        return await msg.edit("Reply to a media to upload it to Cloud.")

    if reply_.file and reply_.file.size > 512 * 1024 * 1024:  # 512 MB
        return await msg.edit("File size Limit is 512 MB.")

    _med = await reply_.download_media()
    if not _med:
        return await msg.edit("Something went wrong.")

    with open(_med, "rb") as f:
        data = f.read()
        resp = requests.post("https://envs.sh", files={"file": data})
        if resp.status_code == 200:
            await msg.edit(f"https://envs.sh/{resp.text}")
        else:
            await msg.edit("Something went wrong. Please try again later.")
