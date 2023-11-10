from bs4 import BeautifulSoup as soup
from requests import get
from telethon import events, Button
from ._config import bot

BASE_URL = "https://www.torlock.com/"


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

    # print(results)

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
                description=i["date"] + " | " + i["size"] + " | " + i["seeds"] + " | " + i["leeches"],
                text=i["url"],
                buttons=[
                    [Button.url("Magnet", await get_torrent_magnet(i["url"]))],
                    [Button.url("Open", i["url"])],
                ],
            )
        )

    await e.answer(articles, switch_pm="Search results for: " + q)

    