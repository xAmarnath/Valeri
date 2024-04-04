import io
import os

import requests
import yt_dlp
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeFilename
from youtubesearchpython import VideosSearch

from ._handler import new_cmd

# Youtube based SONG DOWNLOAD


def search_song(query):
    videosSearch = VideosSearch(query, limit=1)
    result = videosSearch.result()
    if len(result["result"]) == 0:
        return None
    return result["result"][0]


def download_song(link):
    opts = {
        "format": "bestaudio/best",
        "outtmpl": "%(id)s.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            }
        ],
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([link])


@new_cmd(pattern="song")
async def song(e):
    try:
        q = e.text.split(" ", 1)[1]
    except IndexError:
        return await e.reply("Give me a song name.")

    msg = await e.reply("Searching...")
    result = search_song(q)
    if not result:
        return await msg.edit("Song not found.")
    await msg.edit(f"Downloading {result['title']}...")
    download_song(result["link"])

    async with e.client.action(e.chat_id, "audio"):
        with io.BytesIO(requests.get(result["thumbnails"][0]["url"]).content) as thumb:
            thumb.name = "thumb.jpg"
            await e.client.send_file(
                e.chat_id,
                f"{result['id']}.mp3",
                thumb=thumb,
                attributes=[
                    DocumentAttributeAudio(
                        duration=0,
                        title=result["title"],
                        performer=result["channel"]["name"],
                    ),
                    DocumentAttributeFilename(f"{result['title']}.mp3"),
                ],
            )

    await msg.delete()
    os.remove(f"{result['id']}.mp3")
    os.remove(f"{result['id']}.jpg") if os.path.exists(f"{result['id']}.jpg") else ""
