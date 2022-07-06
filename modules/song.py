# song.py

import io

from requests import get
from telethon import types
from PIL import Image

from ._handler import newMsg

HOST = "https://api.roseloverx.tk"


@newMsg(pattern="song")
async def _song(message):
    try:
        query = message.text.split(None, maxsplit=1)[1]
    except IndexError:
        return await message.reply("song query missing.")
    song = search_song(query=query)
    if song is None:
        return await message.reply("song not found.")
    params = {"id": song["id"], "download": "true"}
    response = get(HOST + "/youtube/download", params=params)
    with io.BytesIO(response.content) as file:
        with io.BytesIO(get(song["thumbnail"]).content) as thumb:
            thumb.name = "thumbnail.jpg"
            image = Image.open(thumb)
            thumb = image.resize((320, 320))        # Resize the thumbnail
            file.name = response.headers.get("file-name") or "song.mp3"
            async with message.client.action(message.chat_id, "audio"):
                await message.respond(
                    file=file,
                    attributes=[
                        types.DocumentAttributeAudio(
                            duration=convert_duration(song["duration"]),
                            title=song["title"],
                            performer=song["channel"],
                        )
                    ],
                    thumb=thumb,
                )


@newMsg(pattern="video")
async def _video_dl_youtube(message):
    try:
        query = message.text.split(None, maxsplit=1)[1]
    except IndexError:
        return await message.reply("video query missing.")
    vid = search_song(query=query)
    if vid is None:
        return await message.reply("video result not found.")
    params = {"id": vid["id"], "download": "true", "video": "true"}
    response = get(HOST + "/youtube/download", params=params)
    with io.BytesIO(response.content) as file:
        with io.BytesIO(get(vid["thumbnail"]).content) as thumb:
            thumb.name = "thumbnail.jpg"
            file.name = response.headers.get("file-name") or "video.mp4"
            async with message.client.action(message.chat_id, "video"):
                await message.respond(
                    file=file,
                    attributes=[
                        types.DocumentAttributeVideo(
                            duration=convert_duration(vid["duration"]),
                            w=1280,
                            h=720,
                            supports_streaming=True,
                        )
                    ],
                    thumb=thumb,
                )


def search_song(query):
    """
    Search for a song on youtube and return the first result.
    """
    params = {"q": query}
    request = get(HOST + "/youtube/search", params=params)
    request = request.json() if request.status_code == 200 else {"data": []}
    if len(request["data"]) == 0:
        return None
    return request["data"][0]


def convert_duration(duration):
    """
    Converts a duration in the format of HH:MM:SS to seconds.
    """
    duration = duration.split(":")
    if len(duration) == 3:
        return int(duration[0]) * 60 * 60 + int(duration[1]) * 60 + int(duration[2])
    elif len(duration) == 2:
        return int(duration[0]) * 60 + int(duration[1])
    else:
        return int(duration[0])
