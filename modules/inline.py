import datetime
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
        tex = e.text.split("doge ")[1]
    except IndexError:
        result = [
            e.builder.article(
                "Query missing",
                "Please add a query to search for a doge.",
                link_preview=False,
                text="Doge search query missing." + "\n" + "Usage: `doge <query>`",
            )
        ]
        return await e.answer(result)
    if not tex:
        return
    a = time.time()
    image_1 = write_on_image("doge_write.webp", tex, "doge.ttf", "black", True)
    image_2 = write_on_image("doge_3.webp", tex, "doge.ttf", "black", True)
    image_3 = write_on_image("doge_3.webp", tex, "doge.ttf", "black", True)
    print("time taken to draw: ", time.time() - a)
    await e.answer(
        [
            await e.builder.document(
                image_1,
                title="doge_write.webp",
                description="xd",
            ),
            await e.builder.document(
                image_2,
                title="doge_2.webp",
                description="xd_2",
            ),
            await e.builder.document(
                image_3,
                title="doge_2.webp",
                description="xd_2",
            ),
        ],
        gallery=True,
    )
