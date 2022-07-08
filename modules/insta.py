import io
from os import getenv

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
            w, h = item.get("original_width"), item.get("original_height")
            images = item.get("image_versions2", {}).get("candidates", [])
            for image in images:
                if image.get("width") == w and image.get("height") == h:
                    return (
                        image.get("url", ""),
                        item.get("like_count", 0),
                        item.get("comment_count", 0),
                        item.get("user", {}).get("username", ""),
                        item.get("caption", {}).get("text", ""),
                    )
            return (
                images[0].get("url", ""),
                item.get("like_count", 0),
                item.get("comment_count", 0),
                item.get("user", {}).get("username", ""),
                item.get("caption", {}).get("text", ""),
            )
        elif req.get("items", [])[0].get("media_type") == 2:
            item = req.get("items", [])[0]
            video = item.get("video_versions", [])[0]
            return (
                video.get("url", ""),
                item.get("like_count", 0),
                item.get("comment_count", 0),
                item.get("user", {}).get("username", ""),
                item.get("caption", {}).get("text", ""),
            )
    except (JSONDecodeError, KeyError, IndexError):
        return "", 0, 0, "", ""


@newMsg(pattern="(insta|instagram|instadl|instadownload)")
async def _insta(e):
    if not IG_SESSION:
        await e.reply("`Instagram session not found.`")
        return
    url = await get_text_content(e)
    if not url:
        await e.reply("`Usage: !insta <url>`")
        return
    if not url.startswith("https://www.instagram.com/p/"):
        await e.reply("`Invalid url.`")
        return
    dl_url, likes, comments, username, caption = get_ig_download_url(url)
    if not dl_url:
        await e.reply("`Failed to get the download url.`")
        return
    msg = await e.reply("`Downloading...`")
    with io.BytesIO(get(dl_url, cookies=cookies).content) as f:
        await e.client.send_file(
            e.chat_id,
            f,
            caption=f"**📷 {username}** \n\n💬 {caption} \n\n💬 {comments} \n\n👍 {likes}",
            reply_to=e.id,
        )
    await msg.delete()
