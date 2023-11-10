from requests import get

r = get("https://rogstreamlive.eu.org/hls/tata/play.php?id=562",
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                                    "Chrome/80.0.3987.149 Safari/537.36"})
with open("b.html", "wb") as f:
    f.write(r.content)