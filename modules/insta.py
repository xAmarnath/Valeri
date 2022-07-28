import io
import time
from os import getenv

from requests import JSONDecodeError, get

from ._handler import newMsg
from ._helpers import get_text_content

IG_SESSION = getenv("IG_SESSION", "")

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


cookies = {
    "sessionid": IG_SESSION,
}


def get_ig_download_url(url: str):
    """Get the download url for the media."""
    url = url + "?&__a=1&__d=dis" if not url.endswith("?&__a=1&__d=dis") else url
    try:
        req = get(url, cookies=cookies).json()
        if req.get("items", [])[0].get("media_type") == 1:
            item = req.get("items", [])[0]
            width, hieght = item.get("original_width"), item.get("original_height")
            images = item.get("image_versions2", {}).get("candidates", [])
            for image in images:
                if image.get("width") == width and image.get("height") == hieght:
                    return (
                        image.get("url", ""),
                        item.get("like_count", 0),
                        item.get("comment_count", 0),
                        item.get("user", {}).get("username", "-"),
                        item.get("caption", {}).get("text", "-")
                        if item.get("caption")
                        else "-",
                        item.get("media_type", 0),
                        False,
                    )
            return (
                images[0].get("url", ""),
                item.get("like_count", 0),
                item.get("comment_count", 0),
                item.get("user", {}).get("username", "-"),
                item.get("caption", {}).get("text", "-") if item.get("caption") else "-",
                item.get("media_type", 0),
                False,
            )
        elif req.get("items", [])[0].get("media_type") == 2:
            item = req.get("items", [])[0]
            video = item.get("video_versions", [])[0]
            return (
                video.get("url", ""),
                item.get("like_count", 0),
                item.get("comment_count", 0),
                item.get("user", {}).get("username", "-"),
                item.get("caption", {}).get("text", "-") if item.get("caption") else "-",
                item.get("media_type", 0),
                False,
            )
        else:
            item = req.get("items", [])[0]
            if item.get("carousel_media"):
                urls = [
                    item["carousel_media"][i]["image_versions2"]["candidates"][0]["url"]
                    for i in range(len(item["carousel_media"]))
                ]
                return (
                    urls,
                    item.get("like_count", 0),
                    item.get("comment_count", 0),
                    item.get("user", {}).get("username", "-"),
                    item.get("caption", {}).get("text", "-")
                    if item.get("caption")
                    else "-",
                    item.get("media_type", 0),
                    True,
                )
    except (JSONDecodeError, KeyError, IndexError) as err:
        print(err)
        return "", 0, 0, "", "", 0


@newMsg(pattern="(insta|instagram|instadl|instadownload)")
async def _insta(message):
    # if check_if_spam(message.sender_id):
    # return await message.reply("You are spamming.")
    if not IG_SESSION:
        await message.reply("`Instagram session not found.`")
        return
    url = await get_text_content(message)
    if not url:
        await message.reply("`Usage: !insta <url>`")
        return
    if not url.startswith("https://www.instagram.com"):
        await message.reply("`Invalid url.`")
        return
    (
        dl_url,
        likes,
        comments,
        username,
        caption,
        media_type,
        carousel,
    ) = get_ig_download_url(url)
    caption = caption[:700] if len(caption) > 700 else caption
    if not dl_url:
        await message.reply("`Failed to get the download url.`")
        return
    msg = await message.reply("`Downloading...`")
    caption = "<b>📷 {}</b>\n<i>{}</i>\n<b>Likes:</b> {}\n<b>Comments:</b> {}".format(
        username.upper(), caption, likes, comments
    )
    if carousel:
        dl_bytes = [get(i, cookies=cookies).content for i in dl_url]
        await message.respond(
            caption,
            parse_mode="html",
            file=dl_bytes,
        )
        return await msg.delete()
    with io.BytesIO(get(dl_url, cookies=cookies).content) as f:
        f.name = "instagram.jpg" if media_type == 1 else "instagram.mp4"
        await message.client.send_file(
            message.chat_id, f, caption=caption, parse_mode="html", reply_to=message.id
        )
    await msg.delete()


# TODO : Add insta user search
