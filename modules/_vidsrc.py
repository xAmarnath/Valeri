import re

from bs4 import BeautifulSoup
from requests import get


def get_vid_url(imdb_id):
    url = "https://v2.vidsrc.me/embed/{}".format(imdb_id)
    soup = BeautifulSoup(get(url).text, "html.parser")
    src_hash = soup.find("div", class_="active_source source").get("data-hash")
    headers = {
        "authority": "v2.vidsrc.me",
        "sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        "sec-ch-ua-mobile": "?0",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "navigate",
        "sec-fetch-dest": "iframe",
        "referer": "https://source.vidsrc.me/",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    }

    url = "https://v2.vidsrc.me/src/" + src_hash
    stream_page = get(url, headers=headers, allow_redirects=True)
    m3u8_regex = r"https://.*\.m3u8"
    m3u8_url = re.search(m3u8_regex, stream_page.text).group(0)
    if m3u8_url is None:
        return "Error: No m3u8 url found"
    return m3u8_url
