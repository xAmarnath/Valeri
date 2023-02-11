# song.py

import base64
import io
from urllib.parse import quote

from pyDes import *
from requests import get
from telethon import types

from ._handler import new_cmd
from ._transfers import upload_file

HOST = "https://www.jiosaavn.com/"


@new_cmd(pattern="song")
async def _song(message):
    try:
        query = message.text.split(None, maxsplit=1)[1]
    except IndexError:
        return await message.reply("song query missing.")
    song = search_song(query=query)
    if len(song) == 0:
        return await message.reply("Song not found!")
    response = get(
        get_download_url_hq(song[0].get("more_info", {}).get("encrypted_media_url", ""))
    )
    file = io.BytesIO(response.content)
    with io.BytesIO(get(song[0]["image"]).content) as thumb:
            thumb.name = "thumbnail.jpg"
            # TODO Resize the thumbnail
            file.name = song[0]["id"] + ".m4a"
            async with message.client.action(message.chat_id, "audio"):
                fi = await upload_file(message.client, file)
                file.close()
                await message.respond(
                    "<b>BitRate:</b> 320kbps\n<b>{}</b>".format(song[0]["subtitle"]),
                    parse_mode="html",
                    file=fi,
                    attributes=[
                        types.DocumentAttributeAudio(
                            duration=int(song[0]["more_info"]["duration"]),
                            title=song[0]["title"],
                            performer=song[0]["more_info"]["music"],
                        ),
                        types.DocumentAttributeFilename(
                            file_name=song[0]["id"] + ".m4a"
                        ),
                    ],
                    thumb=thumb,
                )


def search_song(query):
    """
    Search for a song on youtube and return the first result.
    """
    resp = get(
        HOST
        + f"/api.php?_format=json&_marker=0&api_version=4&ctx=web6dot0&__call=search.getResults&p=1&q={quote(query)}"
    )
    results = resp.json().get("results", [])
    return results


def get_download_url(enc):
    des_cipher = des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
    base_url = "http://h.saavncdn.com"
    enc_url = base64.b64decode(enc.strip())
    dec_url = des_cipher.decrypt(enc_url, padmode=PAD_PKCS5).decode("utf-8")
    dec_url = base_url + dec_url.replace("mp3:audios", "") + ".mp3"
    return (
        dec_url.replace("https://aac.saavncdn.com", "")
        .replace(".mp4", "")
        .replace("_96.", ".")
    )


def get_download_url_hq(enc):
    des_cipher = des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
    base_url = "http://h.saavncdn.com"
    enc_url = base64.b64decode(enc.strip())
    dec_url = des_cipher.decrypt(enc_url, padmode=PAD_PKCS5).decode("utf-8")
    dec_url = dec_url.replace("mp3:audios", "")
    return dec_url.replace("_96.", "_320.")


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
