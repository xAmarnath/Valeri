import json
import time
from requests import get, post
from telethon import Button

from ._config import TMDB_KEY as tapiKey
from ._functions import search_imdb, get_weather
from ._handler import newMsg
from ._helpers import gen_random_string, get_text_content, get_user

TELEGRAPH_API_KEY = ""


@newMsg(pattern="(imdb|tmdb)")
async def _imdb_search(e):
    if tapiKey is None:
        return await e.reply("IMDB API key is not set.")
    try:
        query = e.text.split(None, maxsplit=1)[1]
    except IndexError:
        return await e.reply("Provide the title name!")
    caption, url, buttons = search_imdb(query)
    if len(caption) > 1024:
        caption = caption[:1020] + "..."
    await e.reply(caption, file=url, parse_mode="html", buttons=buttons)


@newMsg(pattern="math")
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


@newMsg(pattern="ip")
async def ip_lookup(message):
    ip = await get_text_content(message)
    if ip is None:
        return await message.reply("No IP provided!")
    url = "https://api.roseloverx.tk/ip"
    params = {"ip": ip}
    resp = get(url, params=params)
    resp = resp.json()
    if resp.get('data', {}).get("status", 200) != 200:
        return await message.reply("Error: {}".format(resp.get('data', {}).get("message", "Unknown error")))
    data = resp.get('data', {})
    ip_info = ('<b>IP: <code>{}</code></b>'.format(data.get('ip', '-')) +
               "\nHostname: <code>{}</code></b>".format(data.get('hostname', '-')) +
               "\n<b>City: <code>{}</code></b>".format(data.get('city', '-')) +
               "\n<b>Region: <code>{}</code></b>".format(data.get('region', '-')) +
               "\n<b>Location: <code>{}</code></b>".format(data.get('loc', '-')) +
               "\n<b>Org: <code>{}</code></b>".format(data.get('org', '-')) +
               "\n<b>Postal: <code>{}</code></b>".format(data.get('postal', '-')) +
               "\n<b>Timezone: <code>{}</code></b>".format(data.get('timezone', '-')) +
               "\n<b>Company: <code>{}</code></b>".format(data.get('company', {}).get('name', '-')) +
               "\n<b>Address: <code>{}</code></b>".format(data.get('abuse', {}).get('address', '-')) +
               "\n<b>Email: <code>{}</code></b>".format(data.get('abuse', {}).get('email', '-')) +
               "\n<b>Phone: <code>{}</code></b>".format(data.get('abuse', {}).get('phone', '-')) +
               "\n\n<b>VPN: <code>{}</code></b>".format(data.get('privacy', {}).get('vpn', '-')) +
               "\n<b>Proxy: <code>{}</code></b>".format(data.get('privacy', {}).get('proxy', '-')) +
               "\n<b>Tor: <code>{}</code></b>".format(data.get('privacy', {}).get('tor', '-')) +
               "\n<b>Hosting: <code>{}</code></b>".format(data.get('privacy', {}).get('hosting', '-')) +
               "\n<b>Domains: <code>{}</code></b>".format(' ,'.join(x for x in data.get('domains', {}).get('domains', '[]'))) +
               "\n\n <b>@MissValeri_Bot</b>")
    await message.reply(ip_info, parse_mode="html")


@newMsg(pattern="(weather|w)")
async def weather(message):
    city = await get_text_content(message)
    if city is None:
        return await message.reply("No city provided!")
    response = get_weather(city)
    await message.reply(response)


@newMsg(pattern="ud")
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
    UDICT = "<b>Word:</b> " + word + "\n"
    UDICT += "<b>Definition:</b> " + definition + "\n"
    UDICT += "<b>Example:</b> " + example + "\n"
    UDICT += "<b>Author:</b> " + author + "\n"
    await message.reply(
        UDICT,
        buttons=[
            [
                Button.inline("👍 {}".format(upvote)),
                Button.inline("👎 {}".format(downvote)),
            ]
        ],
        parse_mode="html",
    )


@newMsg(pattern="pinterest")
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
    pins = result.get("resource_response", {}).get(
        "data", {}).get("results", [])
    for pin in pins:
        if pin.get("images", {}).get("orig", {}).get("url", "") != "":
            urls.append(pin.get("images", {}).get("orig", {}).get("url", ""))
        if len(urls) == 4:
            break
    if len(urls) == 0:
        return await message.reply("No results found!")
    await message.reply("Found `{}` results for **{}**:".format(len(pins), query))
    await message.reply(file=urls)


@newMsg(pattern="(fake|faker)")
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
        result.get("location", {}).get("street", "")
        + " "
        + result.get("location", {}).get("city", "")
        + " "
        + result.get("location", {}).get("state", "")
        + " "
        + result.get("location", {}).get("postcode", "")
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
        pasre_mode="html",
    )


@newMsg(pattern="(w|wiki)")
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


@newMsg(pattern="id")
async def id_(message):
    if not message.reply and not len(message.text.split(None)) > 1:
        user = message.sender
    else:
        user, _ = await get_user(message)
    if user is None:
        return await message.reply(
            "Your ID is: ```" + str(message.from_user.id) + "```"
        )
    if message.reply_to:
        r = await message.get_reply_message()
        if r.fwd:
            return await message.reply(
                "The ID of "
                + "Forwarded user"
                + " is: ```"
                + str(r.forward_from.id)
                + "```"
            )
        return await message.reply(
            "The ID of "
            + r.from_user.first_name
            + " is: ```"
            + str(r.from_user.id)
            + "```"
        )
    return await message.reply(
        "The ID of " + user.first_name + " is: ```" + str(user.id) + "```"
    )


@newMsg(pattern="(telegraph|tg)")
async def telegraph_(message):
    media, file = False, ""
    if message.reply_to:
        r = await message.get_reply_message()
        if r.media:
            media = True
            file = await r.download_media()
            caption = r.caption if r.caption else ""
    else:
        caption = await get_text_content(message)
    if caption is None and file == "":
        return await message.reply("No caption or media provided!")

    if media:
        url = telegraph_file_upload(file)
    else:
        url = "https://api.telegra.ph/createPage"
        params = {
            "content": caption,
            "access_token": get_tgf_key(),
            "title": time.strftime("%Y-%m-%d %H:%M:%S"),
            "author_name": "valeri",
            "author_url": "https://t.me/missvaleri_bot",
            "return_content": "false",
        }
        response = get(url, params=params)
        if response.status_code != 200:
            return await message.reply("Error: {}".format(response.status_code))
        result = response.json()
        url = result.get("result", {}).get("url", "")
    await message.reply(
        "Uploaded to <b><a href='{}'>{}</a></b>".format(url, "Telegr.aph"),
        parse_mode="html",
        buttons=[
            [
                Button.url(
                    "View",
                    url,
                ),
            ],
        ],
    )


def get_tgf_key():
    global TELEGRAPH_API_KEY
    if TELEGRAPH_API_KEY != "":
        return TELEGRAPH_API_KEY
    else:
        url = "https://api.telegra.ph/createAccount?short_name={}&author_name=Anonymous".format(
            gen_random_string(10)
        )
        response = get(url)
        if response.status_code != 200:
            return None
        result = response.json()
        token = result.get("result", {}).get("access_token", "")
        TELEGRAPH_API_KEY = token
        return token


def telegraph_file_upload(path_to_file):
    file_types = {
        "gif": "image/gif",
        "jpeg": "image/jpeg",
        "jpg": "image/jpg",
        "png": "image/png",
        "mp4": "video/mp4",
    }
    file_ext = path_to_file.split(".")[-1]

    if file_ext in file_types:
        file_type = file_types[file_ext]
    else:
        return f"error, {file_ext}-file can not be proccessed"

    with open(path_to_file, "rb") as f:
        url = "https://telegra.ph/upload"
        response = post(
            url,
            files={"file": ("file", f, file_type)},
            timeout=1,
            params={"access_token": get_tgf_key()},
        )

    telegraph_url = json.loads(response.content)
    telegraph_url = telegraph_url[0]["src"]
    telegraph_url = f"https://telegra.ph{telegraph_url}"

    return telegraph_url


