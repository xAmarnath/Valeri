import io
import time

from requests import JSONDecodeError, get

from ._handler import new_cmd
from ._helpers import get_text_content

spam = {}


def check_if_spam(user_id: int) -> bool:
    """Check if the user is spam."""
    if user_id in spam:
        if time.time() - spam[user_id] > 20:
            spam.pop(user_id)
            return False
        else:
            return True
    else:
        spam[user_id] = time.time()
        return False



def get_ig_download_url(url: str):
    MAX_RETIRES = 2
    retries = 0
    while retries < MAX_RETIRES:
        try:
            response = get(
                "https:a.ztorr.me/api/insta", params={"url": url}, timeout=10
            )
            if response.status_code != 200:
                retries += 1
                continue
            data = response.json()
            return data
        except JSONDecodeError:
            retries += 1

    return None
        


@new_cmd(pattern="(insta|instagram|instadl|instadownload)")
async def _insta(message):
    url = await get_text_content(message)
    if not url:
        await message.reply("`Usage: !insta <url>`")
        return
    if not url.startswith("https://www.instagram.com"):
        await message.reply("`Invalid url.`")
        return
    if check_if_spam(message.from_id):
        await message.reply("`You are spamming.`")
        return
    
    msg = await message.reply("`Downloading...`")
    data = get_ig_download_url(url)
    if not data:
        await msg.edit("`Failed to download.`")
        return
    
    if len(data["videos"]) == 0 or len(data["images"]) == 0 or data["stories"] == 0 or data["highlights"] == 0:
        await msg.edit("`Failed to download.`")
        return
    
    if data["stories"] > 0:
        try:
            await message.client.send_file(
                message.chat_id,
                data["stories"],
                caption="`Story`",
                reply_to=message.id,
            )
        except:
            for i in data["stories"]:
                await message.client.send_file(
                    message.chat_id,
                    i,
                    caption="`Story`",
                    reply_to=message.id,
                )
    if data["highlights"] > 0:
        try:
            await message.client.send_file(
                message.chat_id,
                data["highlights"],
                caption="`Highlights`",
                reply_to=message.id,
            )
        except:
            for i in data["highlights"]:
                await message.client.send_file(
                    message.chat_id,
                    i,
                    caption="`Highlights`",
                    reply_to=message.id,
                )

    if len(data["videos"]) > 0:
        try:
            await message.client.send_file(
                message.chat_id,
                data["videos"],
                caption="`Video`",
                reply_to=message.id,
            )
        except:
            for i in data["videos"]:
                await message.client.send_file(
                    message.chat_id,
                    i,
                    caption="`Video`",
                    reply_to=message.id,
                )

    if len(data["images"]) > 0:
        try:
            await message.client.send_file(
                message.chat_id,
                data["images"],
                caption="`Image`",
                reply_to=message.id,
            )
        except:
            for i in data["images"]:
                await message.client.send_file(
                    message.chat_id,
                    i,
                    caption="`Image`",
                    reply_to=message.id,
                )

    await msg.delete()