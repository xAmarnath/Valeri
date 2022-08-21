import re

from bs4 import BeautifulSoup
from requests import get


def get_vid_url(imdb_id):
    try:
        url = "https://v2.vidsrc.me/embed/{}".format(imdb_id)
        soup = BeautifulSoup(get(url).text, "html.parser")
<<<<<<< HEAD
        src_hash = soup.find(
            "div", class_="active_source source").get("data-hash")
=======
        src_hash = soup.find("div", class_="active_source source").get("data-hash")
>>>>>>> 802f4cb705cce9836f7d6ffe95d95dfdbcad903b
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
    except Exception as e:
        return "Error: {}".format(e)
<<<<<<< HEAD


def get_vidcloud_stream(id):
    try:
        media_server = BeautifulSoup(get("https://www.2embed.to/embed/imdb/movie?id={}".format(id), headers={'user-agent': 'Mozilla/5.0'}).text, 'html.parser').find(
            'div', class_='media-servers dropdown').find('a')['data-id']
        recaptcha_resp = get(
            "https://recaptcha.harp.workers.dev/?anchor=https%3A%2F%2Fwww.google.com%2Frecaptcha%2Fapi2%2Fanchor%3Far%3D1%26k%3D6Lf2aYsgAAAAAFvU3-ybajmezOYy87U4fcEpWS4C%26co%3DaHR0cHM6Ly93d3cuMmVtYmVkLnRvOjQ0Mw..%26hl%3Den%26v%3DPRMRaAwB3KlylGQR57Dyk-pF%26size%3Dinvisible%26cb%3D7rsdercrealf&reload=https%3A%2F%2Fwww.google.com%2Frecaptcha%2Fapi2%2Freload%3Fk%3D6Lf2aYsgAAAAAFvU3-ybajmezOYy87U4fcEpWS4C").json()['rresp']
        vidcloudresp = get("https://www.2embed.to/ajax/embed/play",
                           params={'id': media_server, '_token': recaptcha_resp})
        rbstream = "https://rabbitstream.net/embed/m-download/{}".format(
            vidcloudresp.json()['link'].split('/')[-1])
        soup = BeautifulSoup(get(rbstream).text, 'html.parser')
        return [a['href'] for a in soup.find('div', class_='download-list').find_all('a')]
    except:
        return None
=======
>>>>>>> 802f4cb705cce9836f7d6ffe95d95dfdbcad903b
