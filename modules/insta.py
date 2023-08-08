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
                "https://a.ztorr.me/api/insta", params={"url": url}, timeout=10
            )
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
    if check_if_spam(message.sender_id):
        await message.reply("`You are spamming.`")
        return

    msg = await message.reply("`Downloading...`")
    data = get_ig_download_url(url)
    if not data:
        await msg.edit("`Failed to download.`")
        return

    if len(data.get("videos", [])) == 0 and len(data.get("images", [])) == 0 and data.get("stories") == 0 and data.get("highlights") == 0:
        await msg.edit("`Failed to download.`")
        return

    async def send_files(chat_id, files, caption):
        try:
            await message.client.send_file(chat_id, files, caption=caption, reply_to=message.id)
        except:
            i = 0
            for file in files:
                if i != len(files) - 1:
                    await message.client.send_file(chat_id, file, reply_to=message.id)
                else:
                    await message.client.send_file(chat_id, file, caption=caption, reply_to=message.id)

    if data.get("stories"):
        caption = "`Story`" if data.get("caption") is None else f"{data['caption']}"
        await send_files(message.chat_id, data["stories"], caption=caption)

    if data.get("highlights"):
        caption = "`Highlights`" if data.get("caption") is None else f"{data['caption']}"
        await send_files(message.chat_id, data["highlights"], caption=caption)

    if data.get("videos"):
        caption = "`Video`" if data.get("caption") is None else f"{data['caption']}"
        await send_files(message.chat_id, data["videos"], caption)

    if data.get("images"):
        caption = "`Image`" if data.get("caption") is None else f"{data['caption']}"
        await send_files(message.chat_id, data["images"], caption)

    await msg.delete()
