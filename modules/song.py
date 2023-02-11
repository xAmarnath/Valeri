# song.py

import io

from requests import get
from telethon import types

from ._handler import new_cmd
from pyDes import *
import base64

HOST = "https://www.jiosaavn.com/"


@new_cmd(pattern="song")
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
            # TODO Resize the thumbnail
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


def search_song(query):
    """
    Search for a song on youtube and return the first result.
    """
    resp = get(HOST+f"/api.php?_format=json&_marker=0&api_version=4&ctx=web6dot0&__call=search.getResults&p=1&q={quote(query)}")
    results = resp.json().get('results', [])
    return results 

def get_download_url(enc):
 des_cipher = des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0" , pad=None, padmode=PAD_PKCS5)
 base_url = 'http://h.saavncdn.com'
 enc_url = base64.b64decode(url.strip())
 dec_url = des_cipher.decrypt(enc_url,padmode=PAD_PKCS5).decode('utf-8')
 dec_url = base_url + dec_url.replace('mp3:audios','') + '.mp3'
 return dec_url.replace('https://aac.saavncdn.com', '').replace('.mp4', '')

    


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
