import time

from mega import Mega

from ._handler import auth_only, newMsg
from ._helpers import human_readable_size as size

mega = Mega()
mega = mega.login("prolikem3@outlook.com", "Mohit@123")


@newMsg(pattern="ulmega")
async def _ul_mega(e):
    r = await e.get_reply_message()
    if not r and not r.media:
        return await e.reply("Reply to a media to ul to mega.nz")
    msg = await e.reply("Downloading...")
    media = await r.download_media()
    msg = await msg.edit("Uploading...")
    startTime = time.time()
    file = mega.upload(media)
    url = mega.get_upload_link(file)
    await msg.edit(
        "**Mega.NZ File**\n\n `{}` \n\n**Time:** `{}s`\n**🎉 @MissValeri_Bot**".format(
            url, round(time.time() - startTime, 2)
        )
    )


@newMsg(pattern="megausage")
async def _mage_usage(e):
    usage = mega.get_storage_space()
    quota = mega.get_quota()
    _usage = "**Mega.NZ Usage**\n\n**Used:** `{}`\n**Free:** `{}`\n**Total:** `{}`\n**Disk Quota:** `{}`\n\n**🎉 @MissValeri_Bot**".format(
        size(usage["used"]),
        size(int(usage["total"]) - int(usage["used"])),
        size(usage["total"]),
        size(quota),
    )
    await e.reply(_usage)


@newMsg(pattern="megafiles")
@auth_only
async def _mega_files(e):
    pass
