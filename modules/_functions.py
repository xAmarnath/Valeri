from urllib.parse import quote

from bs4 import BeautifulSoup
from requests import get, post


def get_imdb_title_with_keyword(keyword: str):
    """Get IMDB title with keyword"""
    url = "https://www.imdb.com/find?ref_=nv_sr_fn&q={}&s=tt".format(keyword)
    response = get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    result = soup.find("td", {"class": "result_text"})
    if result:
        return result.a.attrs["href"].split("/")[2]
    return "No results found"


def get_imdb_soup(keyword: str):
    """Get IMDB soup"""
    imdb_id = get_imdb_title_with_keyword(keyword)
    url = "https://www.imdb.com/title/{}/".format(imdb_id)
    response = get(url)
    return BeautifulSoup(response.text, "html.parser")


def get_weather(city: str):
    """Get weather from openweathermap.org"""
    url = "https://www.timeanddate.com/scripts/completion.php"
    params = {"xd": 21, "query": city, "mode": "ci"}
    response = get(url, params=params)
    if response.text == "":
        return "City not found"
    print(response.text)
    url = "https://www.timeanddate.com" + response.text.split("/ext")[0]
    response = get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    weather = soup.find("div", {"id": "qlook"})
    data = weather.find_all("p")
    stat = data[0].text
    info = str(data[1]).split("<br/>")
    details = [x.text for x in soup.find(class_="bk-focus__info").find_all("td")]
    result = (
        "<b>Weather in <code>{}</code></b>\n\n".format(city)
        + "<b>Temperature:</b> <code>{}</code>\n".format(
            weather.find("div", {"class": "h2"}).text
        )
        + "<b>Status:</b> {}\n".format(stat)
        + "<b>Feels like:</b> <code>{}</code>\n".format(info[0].split(": ")[1])
        + "<b>Forecast:</b> <code>{}</code>\n".format(
            info[1].split(": ")[1].split("<")[0]
        )
        + "<b>Wind:</b> <code>{}</code>\n".format(info[2].split(": ")[1].split("<")[0])
        + "<b>Location:</b> {}\n".format(details[0])
        + "<b>Current Time:</b> <code>{}</code>\n".format(details[1])
        + "<b>Latest Update:</b> <code>{}</code>\n".format(details[2])
        + "<b>Visibility:</b> {}\n".format(details[3])
        + "<b>Pressure:</b> <code>{}</code>\n".format(details[4])
        + "<b>Humidity:</b> <code>{}</code>\n".format(details[5])
        + "<b>Dew Point:</b> <code>{}</code>\n".format(details[6])
        + "\n<b>🎉 @MissValeri_Bot</b>"
    )
    return result


def truecaller(num):
    params = {
        "q": num,
        "countryCode": "+91",
        "type": "4",
        "locAddr": "",
        "placement": "SEARCHRESULTS,HISTORY,DETAILS",
        "encoding": "json",
    }
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "accept-encoding": "gzip",
        "user-agent": "Truecaller/11.75.5 (Android;10)",
        "clientsecret": "lvc22mp3l1sfv6ujg83rd17btt",
        "authorization": "Bearer "
        + "a2i0C--ZjHrjP-gk3zNq11u1KMCWm9I17jsqJ5HHQXbmtmIhx5_vhbIbG6VNirFJ",
    }
    req = get(
        "https://search5-noneu.truecaller.com/v2/search",
        headers=headers,
        params=params,
        timeout=4,
    )
    d = req.json().get("data", [])
    if len(d) == 0:
        return "", None
    tc = ""
    d = d[0]
    if d.get("name", "") != "":
        tc += "**Name:** {}\n".format(d.get("name", "-"))
    tc += f"**Gender:** {d.get('gender', '-')}\n"
    tc += f"**About:** {d.get('about', '-')}\n" if d.get("about", "") != "" else ""
    if len(d.get("internetAddresses", [])) != 0:
        tc += f"**Email:** {d.get('internetAddresses', [])[0].get('id', '-')}\n"
    return tc, d.get("image")


def translate(text, to_lang="en"):
    url = "https://www.google.com/async/translate?vet=12ahUKEwiM3pvpx8z1AhV_SmwGHRb5C5MQqDh6BAgDECY..i&ei=EL_vYYyWFP-UseMPlvKvmAk&client=opera&yv=3"
    data = f"async=translate,sl:auto,tl:{to_lang},st:{quote(text)},id:1643102010421,qc:true,ac:true,_id:tw-async-translate,_pms:s,_fmt:pc"
    headers = {
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 OPR/83.0.4254.19",
    }
    request = post(url, data=data, headers=headers)
    soup = BeautifulSoup(request.text, "html.parser")
    result = soup.find("span", {"id": "tw-answ-target-text"})
    return result.text.capitalize() if result else "vision.google.api returned err."


def ph_info(q):
    txt = f"**phoneNumber:** {q}\n"
    tc, image = truecaller(q)
    txt += tc
    headers = {
        "authority": "www.findandtrace.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "max-age=0",
        "origin": "https://www.findandtrace.com",
        "referer": "https://www.2embed.to/",
        "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    }

    data = {
        "mobilenumber": q,
        "submit": "Trace",
    }

    response = post(
        "https://www.findandtrace.com/trace-mobile-number-location",
        headers=headers,
        data=data,
    )

    soup = BeautifulSoup(response.text, "html.parser")
    basic = soup.find("div", {"id": "order_review"})
    if not basic:
        return "Invalid Number/Not Found"
    if not basic.find_all("tr"):
        return "Invalid Number/Not Found"

    data = {}
    for i in basic.find_all("tr"):
        if i:
            data[i.find("th").text.strip().replace(":", "")] = i.find("td").text.strip()
    next = basic.findNext("div", {"id": "order_review"})
    for i in next.find_all("tr"):
        if i:
            data[i.find("th").text.strip().replace(":", "")] = i.find("td").text.strip()
    if data.get("Connection Status"):
        txt += (
            +"**TelecomCircle:** {TelecomCircle}"
            + "\n"
            + "**Operator:** {Operator}"
            + "\n"
            + "**Service:** {Service}"
            + "\n"
            + "**State:** {State}"
            + "\n"
            + "**SimCard Distributed:** {SimCardDist}"
            + "\n"
            + "**Owner:** {Owner}"
            + "\n"
            + "**Address:** {Address}"
            + "\n"
            + "**Last Login:** {LastLogin}"
            + "\n"
            + "**Last Live Location:** {LastLiveLocation}"
            + "\n"
            + "**Num of Search:** {NumofSearch}"
            + "\n"
            + "**Latest Search Places:** {LatestSearchPlaces}"
            + "\n"
            + "**TelecomCircle Capital:** {TelecomCircleCapital}"
            + "\n"
            + "**Language:** {Language}"
            + "\n"
            + "**Ref Hash:** {RefHash}"
        ).format(
            TelecomCircle=data["Telecoms Circle / State"],
            Operator=data["Original Network (First Alloted)"],
            Service=data["Service Type / Signal"],
            State=data["Connection Status"],
            SimCardDist=data[f'+91 {data["Mobile Phone"]} - SIM card distributed at'],
            Owner=data["Owner / Name of the caller"],
            Address=data["Address / Current GPS Location"],
            LastLogin=data[
                "Last Login Location (Facebook / Google Map / Twitter / Instagram )"
            ],
            LastLiveLocation=data["Last Live location"],
            NumofSearch=data["Number of Search History"],
            LatestSearchPlaces=data["Latest Search Places "],
            TelecomCircleCapital=data["Telecom Circle Capital "],
            Language=data["Main Language in the telecoms circle "],
            RefHash=data["Unique search request Ref "],
        )
    return txt, image
