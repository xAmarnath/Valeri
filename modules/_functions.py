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
    details = [x.text for x in soup.find(
        class_="bk-focus__info").find_all("td")]
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
    return result.text.capitalize() if result else "vision.google.api returned err."

