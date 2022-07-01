from ._handler import newIn
from telethon import events, Button
from ._helpers import human_readable_size
from requests import get
from urllib.parse import quote
import datetime


@newIn(pattern="torrent")
async def _torrent(message: events.InlineQuery.Event):
    try:
        query = message.text.split(maxsplit=1)[1]
    except IndexError:
        result = message.builder.article(
            "Query missing",
            "Please add a query to search for a torrent.",
            link_preview=False,
            text='Torrent search query missing.' + '\n' + 'Usage: `torrent <query>`',
        )
        return await message.answer([result])
    params = {"q": query}
    request = get("https://tpb23.ukpass.co/apibay/q.php", params=params)
    request = request.json()
    results = []
    for result in request:
        if len(results) >= 10:
            break
        magnet = 'magnet:?xt=urn:btih:' + \
            result["info_hash"] + '&dn=' + result["name"]
        buttons = [
            [Button.inline(
                "🌟", data='star_torrent'), ],
            [Button.url(
                "Add to Seedr", url='t.me/missvaleri_bot?start=addtorrent&magnet=' + quote(magnet)), ],
        ]
        results.append(
            message.builder.article(
                result["name"],
                'Seeders: ' + str(result["seeders"]) + '\n' + 'Leechers: ' + str(
                    result["leechers"]) + '\n' + 'Size: ' + str(human_readable_size(int(result["size"]))) + '\n',
                link_preview=False,
                parse_mode="html",
                buttons=buttons,
                text='''✨ <b>{}</b>

Size: {}
Seeders: {}
Leechers: {}
Uploaded On: {}
Num Files: {}

<b>Magnet Link:</b> <code>{}</code>

🔥via @MissValeri_Bot'''.format(result["name"], human_readable_size(int(result["size"])), result["seeders"], result["leechers"], datetime.datetime.fromtimestamp(int(result["added"])).strftime('%Y-%m-%d %H:%M:%S'), result['num_files'], magnet),
            )
        )
    await message.answer(results)
