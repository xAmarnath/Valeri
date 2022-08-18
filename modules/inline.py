import datetime
import threading
import time
from urllib.parse import quote

from requests import get
from telethon import Button, events, types

from ._handler import newIn
from ._helpers import human_readable_size, write_on_image


@newIn(pattern="torrent")
async def _torrent(message: events.InlineQuery.Event):
    try:
        query = message.text.split(maxsplit=1)[1]
    except IndexError:
        result = message.builder.article(
            "Query missing",
            "Please add a query to search for a torrent.",
            link_preview=False,
            text="Torrent search query missing." + "\n" + "Usage: `torrent <query>`",
        )
        return await message.answer([result])
    request = get("https://tpb23.ukpass.co/apibay/q.php?q=" + quote(query))
    request = request.json()
    results = []
    for result in request:
        if len(results) >= 10:
            break
        magnet = "magnet:?xt=urn:btih:" + result["info_hash"] + "&dn=" + result["name"]
        buttons = [
            [
                Button.inline("🌟", data="star_torrent"),
            ],
            [
                Button.url(
                    "Add to Seedr",
                    url="t.me/missvaleri_bot?start=addtorrent&magnet=" + quote(magnet),
                ),
            ],
        ]
        results.append(
            message.builder.article(
                result["name"],
                "Seeders: "
                + str(result["seeders"])
                + "\n"
                + "Leechers: "
                + str(result["leechers"])
                + "\n"
                + "Size: "
                + str(human_readable_size(int(result["size"])))
                + "\n",
                link_preview=False,
                parse_mode="html",
                buttons=buttons,
                text="""✨ <b>{}</b>

Size: {}
Seeders: {}
Leechers: {}
Uploaded On: {}
Num Files: {}

<b>Magnet Link:</b> <code>{}</code>

🔥via @MissValeri_Bot""".format(
                    result["name"],
                    human_readable_size(int(result["size"])),
                    result["seeders"],
                    result["leechers"],
                    datetime.datetime.fromtimestamp(int(result["added"])).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    result["num_files"],
                    magnet,
                ),
            )
        )
    await message.answer(results)


@newIn(pattern="geo ?(.*)")
async def geo_search_(e):
    q = e.pattern_match.group(1)
    if not q:
        return
    thumb = types.InputWebDocument(
        url="https://telegra.ph/file/da565819d3f99e43fecec.jpg",
        size=1423,
        mime_type="image/jpeg",
        attributes=[],
    )
    url = f"http://dev.virtualearth.net/REST/v1/Autosuggest?query={q}&key=AsVuFq5LexGs3arw0czJopBSoYAdCuJroMLXnAa7SugcRjR1ulFGikBR-DYOcxs2"
    r = get(url)
    try:
        r = r.json().get("resourceSets")[0].get("resources")[0].get("value")
    except (IndexError, KeyError):
        return
    c = ["1", "2", "3", "4", "5"]
    pop_list = []
    for x in r:
        if len(pop_list) == 5:
            break
        pic_link = f"https://dev.virtualearth.net/REST/v1/Imagery/Map/Road/{quote(q)}?mapSize=500,500&key=AsVuFq5LexGs3arw0czJopBSoYAdCuJroMLXnAa7SugcRjR1ulFGikBR-DYOcxs2"
        a = x.get("address")
        title = a.get("locality")
        description = a.get("formattedAddress")
        text = f"**[{description}]**({pic_link})\n**Locality:** {title}\n**State:** {a.get('adminDistrict')}\n**Country:** {a.get('countryRegion')}, {a.get('countryRegionIso2')}"
        pop_list.append(
            await e.builder.article(
                title=str(c[len(pop_list)]) + ". " + str(title),
                description=str(description),
                text=text,
                thumb=thumb,
                link_preview=True,
                buttons=[
                    [Button.inline(title or "Map", data=f"geo_{description[:30]}")],
                    [
                        Button.switch_inline(
                            "Search Again", query="geo ", same_peer=True
                        )
                    ],
                ],
            )
        )
    await e.answer(pop_list)


@newIn(pattern="doge ?(.*)")
async def doge_write_on_sticker(e: events.InlineQuery.Event):
    try:
        if "doge" in e.text:
            tex = e.text.split("doge ")[1]
        else:
            tex = e.text
    except IndexError:
        return await e.answer(
            [
                e.builder.article(
                    "Query missing",
                    "Please add a query to search for a doge.",
                    link_preview=False,
                    text="Doge search query missing." + "\n" + "Usage: `doge <query>`",
                )
            ]
        )
    if not tex:
        return
    images = []
    time.time()
    threads = [
        threading.Thread(
            target=write_on_image,
            args=("doge_write.webp", tex, "doge.ttf", "black", images),
        ),
        threading.Thread(
            target=write_on_image,
            args=("doge_2.webp", tex, "doge.ttf", "black", images),
        ),
        threading.Thread(
            target=write_on_image,
            args=("doge_3.webp", tex, "doge.ttf", "black", images),
        ),
        threading.Thread(
            target=write_on_image,
            args=("doge_4.webp", tex, "doge.ttf", "black", images),
        ),
    ]
    [t.start() for t in threads]
    [t.join() for t in threads]
    await e.answer(
        [
            await e.builder.document(
                images[0],
                title="doge_write.webp",
                description="xd_1",
                text="🥵",
            ),
            await e.builder.document(
                images[1],
                title="doge_2.webp",
                description="xd_2",
                text="😭",
            ),
            await e.builder.document(
                images[2],
                title="doge_3.webp",
                description="xd_3",
                text="🤧",
            ),
            await e.builder.document(
                images[3],
                title="doge_4.webp",
                description="xd_4",
                text="🙂",
            ),
        ],
        gallery=True,
    )


@newIn(pattern="imdb ?(.*)")
async def imdb_inline_query(e):
    try:
        query = e.text.split(None, maxsplit=1)[1]
    except:
        return
    url = "https://watch-series-go.vercel.app/api/imdb"
    req = get(url, params={"query": query}).json()
    results = []
    for title in req:
        results.append(
            e.builder.photo(
                file=title.get("poster"),
                force_document=True,
                title=f"{title.get('title', '-')} ({title.get('year')}",
                text=f"{title.get('title', '-')} ({title.get('year')}",
                buttons=Button.inline("ViewInsideTG", data="vimdb_{}".format(title.get("id"))),
            )
        ) if title.get("poster") else None
    await e.answer(results)
