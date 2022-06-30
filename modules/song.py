import io

from requests import get
from telethon.types import DocumentAttributeAudio

from ._handler import newMsg

HOST = "https://api.roseloverx.tk/youtube/download"


@newMsg(pattern="song")
async def _song(e):
    try:
        q = e.text.split(None, maxsplit=1)[1]
    except IndexError:
        return await e.reply("song query missing.")
    params = {"query": q, "download": "true"}
    r = get(HOST, params=params)
    with io.BytesIO(r.content) as file:
        file.name = r.headers.get("file-name") or "song.mp3"
        await e.respond(file=file, attributes=[DocumentAttributeAudio(60, performer='RoseLover')])
