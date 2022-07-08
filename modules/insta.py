import io
from os import getenv
from pprint import pprint

from requests import JSONDecodeError, get

from ._handler import newMsg
from ._helpers import get_text_content

IG_SESSION = getenv("IG_SESSION", "")

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
            if item.get("carousel_media_count") > 1:
                print("Carousel")
            w, h = item.get("original_width"), item.get("original_height")
            images = item.get("image_versions2", {}).get("candidates", [])
            for image in images:
                if image.get("width") == w and image.get("height") == h:
                    x = (
                        image.get("url", ""),
                        item.get("like_count", 0),
                        item.get("comment_count", 0),
                        item.get("user", {}).get("username", ""),
                        item.get("caption", {}).get("text", "")
                        if item.get("caption")
                        else "",
                        item.get("media_type", 0),
                    )
                    print(x)
                    return x
            x = (
                images[0].get("url", ""),
                item.get("like_count", 0),
                item.get("comment_count", 0),
                item.get("user", {}).get("username", ""),
                item.get("caption", {}).get("text", "") if item.get("caption") else "",
                item.get("media_type", 0),
            )
            print(x)
            return x
        elif req.get("items", [])[0].get("media_type") == 2:
            item = req.get("items", [])[0]
            video = item.get("video_versions", [])[0]
            return (
                video.get("url", ""),
                item.get("like_count", 0),
                item.get("comment_count", 0),
                item.get("user", {}).get("username", ""),
                item.get("caption", {}).get("text", "") if item.get("caption") else "",
                item.get("media_type", 0),
            )
        else:
            pprint(req)
            return (
                "",
                0,
                0,
                "",
                "",
                0,
            )
    except (JSONDecodeError, KeyError, IndexError) as err:
        print(err)
        return "", 0, 0, "", "", 0


@newMsg(pattern="(insta|instagram|instadl|instadownload)")
async def _insta(message):
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
    ) = get_ig_download_url(url)
    if not dl_url:
        await message.reply("`Failed to get the download url.`")
        return
    msg = await message.reply("`Downloading...`")
    caption = "<b>📷 {}</b>\n<i>{}</i>\n<b>Likes:</b> {}\n<b>Comments:</b> {}".format(
        username.upper(), caption, likes, comments
    )
    with io.BytesIO(get(dl_url, cookies=cookies).content) as f:
        f.name = "instagram.jpg" if media_type == 1 else "instagram.mp4"
        await message.client.send_file(
            message.chat_id, f, caption=caption, parse_mode="html", reply_to=message.id
        )
    await msg.delete()
