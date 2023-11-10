from bs4 import BeautifulSoup as soup
from requests import get
from telethon import events, Button
from ._config import bot
import uuid

BASE_URL = "https://www.torlock.com"


def search_torrents(q):
    if not q or q == "":
        r = get(BASE_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)

        s = soup(r.text, "html.parser")
        results = []

        for i in s.find_all("a", href=True):
            if i["href"].startswith("/torrent/"):
                try:
                    results.append(
                        {
                            "name": i.text,
                            "url": BASE_URL + i["href"],
                            "date": i.find_next("td").text,
                            "size": i.find_next("td").find_next("td").text,
                            "seeds": i.find_next("td")
                            .find_next("td")
                            .find_next("td")
                            .text,
                            "leeches": i.find_next("td")
                            .find_next("td")
                            .find_next("td")
                            .find_next("td")
                            .text,
                        }
                    )
                except:
                    pass

        return results, None

    r = get(
        BASE_URL + "?qq=1&q=avatar", headers={"User-Agent": "Mozilla/5.0"}, timeout=10
    )

    if r.status_code != 200:
        return None, "Error: " + str(r.status_code)

    s = soup(r.text, "html.parser")
    results = []

    for i in s.find_all("a", href=True):
        if i["href"].startswith("/torrent/"):
            try:
                results.append(
                    {
                        "name": i.text,
                        "url": BASE_URL + i["href"],
                        "date": i.find_next("td").text,
                        "size": i.find_next("td").find_next("td").text,
                        "seeds": i.find_next("td").find_next("td").find_next("td").text,
                        "leeches": i.find_next("td")
                        .find_next("td")
                        .find_next("td")
                        .find_next("td")
                        .text,
                    }
                )
            except:
                pass

    return results, None


def get_torrent_magnet(url):
    r = get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)

    if r.status_code != 200:
        return None, "Error: " + str(r.status_code)

    s = soup(r.text, "html.parser")

    for i in s.find_all("a", href=True):
        if i["href"].startswith("magnet:"):
            return i["href"], None

    return None, "Error: Magnet not found"


def gen_unique_id():
    return str(uuid.uuid4())


search_cache = {}


@bot.on(events.NewMessage(pattern="/t (.*)"))
async def torrent(e):
    try:
        q = e.text.split(" ", 1)[1]
    except IndexError:
        await e.reply("Usage: /t <query>")
        return

    results, err = search_torrents(q)

    if not results:
        await e.reply("No results")
        return

    buttons = []
    btns = []
    bc = 0
    msg = f"Search results for: {q}\n\n"
    q = 0
    for i in results:
        if q > 15:
            break
        q += 1
        msg += f"( {q} ) <b><a href='{i['url']}'>{i['name']}</a></b>\n"
        uq = gen_unique_id()
        search_cache[uq] = i
        btns.append(Button.inline(f"{q}", data=f"t {q}|{uq}"))
        bc += 1
        if bc == 6:
            buttons.append(btns)
            btns = []
            bc = 0
    if bc > 0:
        buttons.append(btns)

    await e.reply(msg, buttons=buttons, link_preview=False, parse_mode="html")


@bot.on(events.CallbackQuery(pattern=r"t"))
async def callback_torrent(e):
    try:
        x = e.data.decode().split(" ", 1)[1]
        q = int(x.split("|")[0])
        link = x.split("|")[1]
    except IndexError:
        await e.answer("Invalid link")
        return
    try:
        url = search_cache[link]["url"]
    except KeyError:
        await e.answer("Cache expired, search again")
        return
    
    print(url)

    magnet, err = get_torrent_magnet(url)

    await e.respond(
        "**#MagnetLink**\n\n`" + magnet + "`"
    )


@bot.on(events.InlineQuery(pattern=r"t (.*)"))
async def inline_torrent(e):
    q = e.pattern_match.group(1)
    results, err = search_torrents(q)

    if err:
        await e.answer([e.builder.article("Error", text=err)])
        return

    if not results:
        await e.answer([e.builder.article("Error", text="No results")])
        return

    articles = []

    for i in results:
        articles.append(
            e.builder.article(
                title=i["name"],
                description=i["date"]
                + " | "
                + i["size"]
                + " | "
                + i["seeds"]
                + " | "
                + i["leeches"],
                text=i["url"],
                buttons=[
                    [Button.url("Magnet", "https://google.com")],
                    [Button.url("Open", i["url"])],
                ],
            )
        )

    await e.answer(articles, switch_pm="Search results for: " + q)
