import io
import json
import os
from random import choice, randint
from urllib.parse import quote

from bs4 import BeautifulSoup
from requests import get, post
from telethon import Button, types

from ._functions import get_imdb_soup, get_weather, translate
from ._handler import new_cmd
from ._helpers import get_text_content, get_user


@new_cmd(pattern="math")
async def math(message):
    exp = await get_text_content(message)
    if exp is None:
        return await message.reply("No expression provided!")
    url = "https://evaluate-expression.p.rapidapi.com"
    headers = {
        "x-rapidapi-host": "evaluate-expression.p.rapidapi.com",
        "x-rapidapi-key": "cf9e67ea99mshecc7e1ddb8e93d1p1b9e04jsn3f1bb9103c3f",
    }
    params = {"expression": exp}
    response = get(url, headers=headers, params=params)
    if response.status_code != 200:
        return await message.reply("Error: {}".format(response.status_code))
    result = response.text
    result = "not found" if result == "" else result
    await message.reply(result)


@new_cmd(pattern="ip")
async def ip_lookup(message):
    ip = await get_text_content(message)
    if ip is None:
        return await message.reply("No IP provided!")
    url = "https://api.roseloverx.tk/ip"
    params = {"ip": ip}
    resp = get(url, params=params)
    resp = resp.json()
    if resp.get("data", {}).get("status", 200) != 200:
        return await message.reply(
            "Error: {}".format(resp.get("data", {}).get("message", "Unknown error"))
        )
    data = resp.get("data", {})
    ip_info = (
        "<b>IP: <code>{}</code></b>".format(data.get("ip", "-"))
        + "\nHostname: <code>{}</code></b>".format(data.get("hostname", "-"))
        + "\n<b>City: <code>{}</code></b>".format(data.get("city", "-"))
        + "\n<b>Region: <code>{}</code></b>".format(data.get("region", "-"))
        + "\n<b>Location: <code>{}</code></b>".format(data.get("loc", "-"))
        + "\n<b>Org: <code>{}</code></b>".format(data.get("org", "-"))
        + "\n<b>Postal: <code>{}</code></b>".format(data.get("postal", "-"))
        + "\n<b>Timezone: <code>{}</code></b>".format(data.get("timezone", "-"))
        + "\n<b>Company: <code>{}</code></b>".format(
            data.get("company", {}).get("name", "-")
        )
        + "\n<b>Address: <code>{}</code></b>".format(
            data.get("abuse", {}).get("address", "-")
        )
        + "\n<b>Email: <code>{}</code></b>".format(
            data.get("abuse", {}).get("email", "-")
        )
        + "\n<b>Phone: <code>{}</code></b>".format(
            data.get("abuse", {}).get("phone", "-")
        )
        + "\n\n<b>VPN: <code>{}</code></b>".format(
            data.get("privacy", {}).get("vpn", "-")
        )
        + "\n<b>Proxy: <code>{}</code></b>".format(
            data.get("privacy", {}).get("proxy", "-")
        )
        + "\n<b>Tor: <code>{}</code></b>".format(
            data.get("privacy", {}).get("tor", "-")
        )
        + "\n<b>Hosting: <code>{}</code></b>".format(
            data.get("privacy", {}).get("hosting", "-")
        )
        + "\n<b>Domains: <code>{}.</code></b>".format(
            " ,".join(x for x in data.get("domains", {}).get("domains", "[]"))
        )
        + "\n\n <b>@MissValeri_Bot</b>"
    )
    await message.reply(ip_info, parse_mode="html")


@new_cmd(pattern="(weather|w)")
async def weather(message):
    city = await get_text_content(message)
    if city is None:
        return await message.reply("No city provided!")
    response = get_weather(city)
    await message.reply(response, parse_mode="html")


@new_cmd(pattern="ud")
async def urban_dictionary(message):
    word = await get_text_content(message)
    if word is None:
        return await message.reply("No word provided!")
    url = "https://api.urbandictionary.com/v0/define"
    params = {"term": word}
    response = get(url, params=params)
    if response.status_code != 200:
        return await message.reply("Error: {}".format(response.status_code))
    result = response.json()
    if len(result["list"]) == 0:
        return await message.reply("No results found!")
    result = result.get("list", [])[0]
    definition = result.get("definition", "-")
    example = result.get("example", "-")
    upvote = result.get("thumbs_up", "-")
    downvote = result.get("thumbs_down", "-")
    author = result.get("author", "-")
    word = result.get("word", "-")
    udict = (
        "<b>Word:</b> "
        + word
        + "\n"
        + "<b>Definition:</b> "
        + definition
        + "\n"
        + "<b>Example:</b> "
        + example
        + "\n"
        + "<b>Author:</b> "
        + author
        + "\n"
    )
    await message.reply(
        udict,
        buttons=[
            [
                Button.inline("👍 {}".format(upvote)),
                Button.inline("👎 {}".format(downvote)),
            ]
        ],
        parse_mode="html",
    )


@new_cmd(pattern="pinterest")
async def pinterest(message):
    query = await get_text_content(message)
    if query is None:
        return await message.reply("No query provided!")
    url = "https://in.pinterest.com/resource/BaseSearchResource/get/"
    params = {
        "source_url": "/search/pins/?q=Avengers&rs=typed&term_meta[]=Avengers%7Ctyped",
        "data": '{"options":{"article":null,"applied_filters":null,"appliedProductFilters":"---","auto_correction_disabled":false,"corpus":null,"customized_rerank_type":null,"filters":null,"query":"'
        + query
        + '","query_pin_sigs":null,"redux_normalize_feed":true,"rs":"typed","scope":"pins","source_id":null,"no_fetch_context_on_resource":false},"context":{}}',
        "_": "1657012830705",
    }
    headers = {
        "authority": "in.pinterest.com",
        "accept": "application/json, text/javascript, */*, q=0.01",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "x-app-version": "e6a3b50",
        "x-pinterest-source-url": "/search/pins/?q=Avengers&rs=typed&term_meta[]=Avengers%7Ctyped",
    }
    response = get(url, params=params, headers=headers)
    result = response.json()
    if result.get("resource_response", {}).get("status", "") != "success":
        return await message.reply("No results found!")
    urls = []
    pins = result.get("resource_response", {}).get("data", {}).get("results", [])
    for pin in pins:
        if pin.get("images", {}).get("orig", {}).get("url", "") != "":
            urls.append(pin.get("images", {}).get("orig", {}).get("url", ""))
        if len(urls) == 4:
            break
    if len(urls) == 0:
        return await message.reply("No results found!")
    await message.reply(
        "Found `{}` results for **{}**:".format(len(pins), query),
        buttons=[
            [
                Button.url(
                    "🔎 View on Pinterest",
                    "https://in.pinterest.com/search/pins/?q=" + quote(query),
                )
            ]
        ],
        parse_mode="md",
    )
    await message.reply(file=urls)


@new_cmd(pattern="(fake|faker)")
async def fake(message):
    country = await get_text_content(message)
    if country is None:
        country = "us"
    url = "https://randomuser.me/api"
    params = {
        "results": 1,
        "nat": country,
    }
    response = get(url, params=params)
    if response.status_code != 200:
        return await message.reply("Error: {}".format(response.status_code))
    result = response.json()
    result = result.get("results", [])[0]
    name = (
        result.get("name", {}).get("first", "")
        + " "
        + result.get("name", {}).get("last", "")
    )
    email = result.get("email", "")
    phone = result.get("phone", "")
    dob = result.get("dob", {}).get("date", "")
    gender = result.get("gender", "")
    address = (
        str(result.get("location", {}).get("street", ""))
        + " "
        + str(result.get("location", {}).get("city", ""))
        + " "
        + str(result.get("location", {}).get("state", ""))
        + " "
        + str(result.get("location", {}).get("postcode", ""))
    )
    await message.reply(
        "<b>Fake Generator</b>\n\n<b>Name:</b> "
        + name
        + "\n<b>Email:</b> "
        + email
        + "\n<b>Phone:</b> "
        + phone
        + "\n<b>DOB:</b> "
        + dob
        + "\n<b>Address:</b> "
        + address
        + "\n<b>Gender:</b> "
        + gender,
        parse_mode="html",
    )


@new_cmd(pattern="realaddr")
async def _raddr(msg):
    query = await get_text_content(msg)
    if query is None:
        return await msg.reply("No query was given!")
    url = "https://www.google.com/search"
    params = {"q": "foodplace near " + query}
    response = get(url, params=params)
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    for result in soup.find_all(class_="X7NTVe"):
        for i in result.find_all("a"):
            if not i.text == "":
                name = i.find(class_="BNeawe deIvCb AP7Wnd").text
                address = BeautifulSoup(str(i).split("<br/>")[1], "html.parser").text
            results.append("<b>{}</b>\n{}".format(name, address))
    if len(results) == 0:
        return await msg.reply("No results found!")
    await msg.reply(
        "Found <code>{}</code> results for <b>{}</b>:\n\n{}".format(
            len(results), query, "\n\n".join(results)
        ),
        buttons=[
            [
                Button.url(
                    "🔎 View on Google",
                    "https://www.google.com/search?q=foodplaces+near+" + quote(query),
                )
            ]
        ],
        parse_mode="html",
    )


@new_cmd(pattern="(w|wiki)")
async def wiki_(message):
    query = await get_text_content(message=message)
    if query is None:
        return await message.reply("No query provided")
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "format": "json",
        "action": "query",
        "prop": "extracts|pageimages",
        "exintro": "",
        "explaintext": "",
        "generator": "search",
        "gsrsearch": "intitle:" + query,
    }
    response = get(url, params=params)
    if response.status_code != 200:
        return await message.reply("Error: {}".format(response.status_code))
    result = response.json()
    result = result.get("query", {}).get("pages", [])
    if len(result) == 0:
        return await message.reply("No results found!")
    result = result[0]
    title = result.get("title", "")
    extract = result.get("extract", "")
    image = result.get("thumbnail", {}).get("source", "")
    if len(extract) > 900:
        extract = extract[:900] + "..."
    await message.reply(
        "<b>Wikipedia</b>\n\n<b>Title:</b> " + title + "\n<b>Extract:</b> " + extract,
        parse_mode="html",
        file=image if image else None,
        buttons=[
            [
                Button.url(
                    "Read More",
                    "https://en.wikipedia.org/wiki/" + title.replace(" ", "_"),
                ),
            ],
        ],
    )


@new_cmd(pattern="carbon")
async def _carbon(message):
    text = await get_text_content(message)
    if text is None:
        return await message.reply("No text provided")
    url = "https://carbonnowsh.herokuapp.com"
    params = {
        "code": text,
        "backgroundColor": "rgba({},{},{},100)".format(
            randint(0, 255), randint(0, 255), randint(0, 255)
        ),
        "fontColor": "rgba({},{},{},100)".format(
            randint(0, 255), randint(0, 255), randint(0, 255)
        ),
        "exportSize": "3x",
        "fontFamily": choice(["Fira Code", "Hack", "JetBrains Mono"]),
        "theme": choice(
            [
                "seti",
                "nord",
                "night owl",
                "panda",
                "vscode",
                "dracula",
                "yeti",
                "twilight",
            ]
        ),
    }
    response = get(url, params=params, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        return await message.reply("CarbonNowsh is down!")
    with io.BytesIO(response.content) as file:
        file.name = "carbon.png"
        await message.reply(file=file)


@new_cmd(pattern="id")
async def id_(message):
    if not message.reply or not len(message.text.split(None)) > 1:
        user = message.sender
    else:
        user, _ = await get_user(message)
    if user is None:
        return await message.reply(
            "Your ID is: ```" + str(message.from_user.id) + "```"
        )
    return await message.reply(
        "The ID of " + user.first_name + " is: ```" + str(user.id) + "```"
    )


@new_cmd(pattern="paste")
async def paste_(message):
    content = await get_text_content(message)
    if content is None:
        if not message.reply:
            return await message.reply("No text provided")
        else:
            r = await message.get_reply_message()
            if r.media:
                file = await r.download_media()
                with open(file, "r", errors="ignore", encoding="utf-8") as f:
                    content = f.read()
                os.remove(file)
            else:
                return await message.reply(
                    "No text provided, supported flags: **-n** [nekobin], **-h** [hastebin], **-r** [rentry], **-s** [spacebin]"
                )
    arg, content = paste_mode(
        message.text.split(None, 1)[1].split(None)
        if len(message.text.split(None)) > 1
        else [],
        content,
    )
    try:
        if arg == "h":
            resp = post(
                url="https://www.toptal.com/developers/hastebin/documents",
                data=content,
                timeout=5,
            )
            url = "https://www.toptal.com/developers/hastebin/" + resp.json()["key"]
            paste_name = "Hastebin"
        elif arg == "s":
            req = post(
                url="https://spaceb.in/api/v1/documents/",
                data={"content": content, "extension": "txt"},
                timeout=5,
            )
            url = "https://spaceb.in/" + req.json()["payload"]["id"]
            paste_name = "Spacebin"
        elif arg == "n":
            req = post(
                url="https://warm-anchorage-15807.herokuapp.com/api/documents",
                json={"content": content},
                timeout=5,
            )
            url = (
                "https://warm-anchorage-15807.herokuapp.com/"
                + req.json()["result"]["key"]
            )
            paste_name = "Nekobin"
    except TimeoutError:
        return await message.reply("Paste failed, server timeout")
    await message.reply(
        "<b>Pasted to <a href='" + url + "'>" + paste_name + "</a></b>",
        parse_mode="html",
        buttons=[
            [
                Button.url(
                    paste_name,
                    url,
                ),
            ],
        ],
        link_preview=False,
    )


def paste_mode(args, content: str):
    """Returns the paste mode and the content"""
    for arg in args:
        for p in [
            ["-n", "--nekobin"],
            ["-s", "--spacebin"],
            ["-h", "--hastebin"],
        ]:
            if arg == p[0]:
                return p[0].split("-")[1], content.replace(p[0], "", 1)
            elif arg == p[1]:
                return p[0].split("-")[1], content.replace(p[1], "", 1)
    return "n", content


@new_cmd(pattern="(tl|tr|translate)")
async def _tl(msg):
    text = await get_text_content(message=msg)
    if text is None:
        return await msg.reply("No text provided to translate")
    if msg.reply_to and len(msg.text.split(None)) > 1:
        to_lang = msg.text.split(None)[1]
    else:
        langs = text.split(None)
        if len(langs[0]) == 2:
            to_lang = langs[0]
            text = text.replace(to_lang, "")
        else:
            to_lang = "en"
    tl = translate(text, to_lang)
    if tl == "":
        return await msg.reply("No such language code exist!")
    await msg.reply(
        "<b>🎉 Translated to {}</b>\n\n<code>{}</code>".format(to_lang, tl),
        parse_mode="html",
    )


@new_cmd(pattern="(gif|giphy)")
async def _gif(msg):
    text = await get_text_content(message=msg)
    if text is None:
        return await msg.reply("No text provided to search for gif")
    url = "https://api.giphy.com/v1/videos/search"
    params = {"q": text, "api_key": "Gc7131jiJuvI7IdN0HZ1D7nh0ow5BU6g"}
    gifs = []
    for gif in get(url, params=params).json()["data"]:
        url = gif.get("images", {}).get("original", {}).get("url")
        if url:
            gifs.append(url)
        if len(gifs) > 4:
            break
    if len(gifs) == 0:
        return await msg.reply("No gifs found")
    gifs_bytes = [io.BytesIO(get(gif).content) for gif in gifs]
    for x in range(len(gifs_bytes)):
        gifs_bytes[x].name = "gif" + str(x) + ".mp4"
    await msg.reply(
        file=gifs_bytes,
        attributes=[
            types.DocumentAttributeAnimated(),
            types.DocumentAttributeFilename(file_name="giphy.gif"),
        ],
    )


@new_cmd(pattern="(imdb|movie)")
async def _imdb(msg):
    text = await get_text_content(message=msg)
    if text is None:
        return await msg.reply("No text provided to search for movie")
    soup = get_imdb_soup(text)
    jsonD = soup.find("script", type="application/ld+json").text
    js = json.loads(jsonD)
    js["sameAs"] = [
        x.text
        for x in soup.find_all(
            class_="ipc-poster-card__title ipc-poster-card__title--clamp-2 ipc-poster-card__title--clickable"
        )
    ]
    js["creator"] = [
        i
        for i in [
            (x.get("name", "-") if x.get("@type") == "Person" else None)
            for x in js.get("creator", [])
        ]
        if i
    ]
    imdb_title = (
        "<b>"
        + js.get("name", "No title")
        + "</b>"
        + "\n<b>Rating:</b> <code>"
        + str(js.get("aggregateRating", {}).get("ratingValue", "-"))
        + "/10</code>"
        + "\n<b>Genres:</b> "
        + ", ".join(["#" + x for x in js.get("genre", [])])
        + ""
        + "\n<b>Cast:</b> "
        + ", ".join([x.get("name", "-") for x in js.get("actor", [])])
        + ""
        + "\n<b>Type:</b> <code>"
        + js.get("type", "-")
        + "</code>"
        + "\n<b>Release date:</b> <code>"
        + js.get("datePublished", "-")
        + "</code>"
        + "\n<b>Description:</b> <u>"
        + js.get("description", "-")
        + "</u>"
        + "\n<b>Content rating:</b> "
        + js.get("contentRating", "-")
        + "\n<b>Creators:</b> <code>"
        + ", ".join(js.get("creator", []))
        + "</code>"
        + "\n<b>Tags:</b> "
        + js.get("keywords", "")
        + "\n<b>Similar:</b> <b><i>"
        + ", ".join(js.get("sameAs", []))
        + "</i></b>"
    )
    poster_url = js.get("image", None)
    trailer_url = "https://imdb.com" + js.get("trailer", {}).get("embedUrl", "")
    buttons = [
        [
            Button.url(
                "IMDB",
                "https://imdb.com" + js.get("url", ""),
            )
        ],
        [
            Button.url(
                "Trailer",
                trailer_url,
            )
        ],
    ]
    await msg.reply(
        imdb_title,
        parse_mode="html",
        buttons=buttons,
        link_preview=False,
        file=poster_url,
    )


@new_cmd(pattern="(dog|dogfact|dogfacts)")
async def _dog_facts(msg):
    url = "https://dog-api.kinduff.com/api/facts"
    data = get(url).json()
    fact = f"""
    <b>Dog Fact</b>
    <code>{data["facts"][0]}</code>
    """
    await msg.reply(fact, parse_mode="html")


@new_cmd(pattern="blerp")
async def blerp_audio(msg):
    query = await get_text_content(msg)
    if not query:
        return await msg.reply("Query not given.")
    try:
        srC = BeautifulSoup(
            get(
                "https://blerp.com"
                + BeautifulSoup(
                    get("https://blerp.com/search", params={"q": query, "r": "R"}).text,
                    "html.parser",
                )
                .find(class_="GlobalSearchWeb__BlerpGridContainer-sc-2gff2k-0 dlEGMi")
                .find("a", href=True)["href"]
            ).text,
            "html.parser",
        ).find("meta", attrs={"name": "twitter:player:stream"})["content"]
    except Exception as err:
        return await msg.reply(str(err))
    async with msg.client.action(e.chat, "audio"):
        await msg.reply(file=srC)
