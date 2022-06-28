from turtle import title
from urllib.parse import quote

from requests import get

from ._config import TMDB_KEY as tapiKey
from ._handler import newMsg


@newMsg(pattern="(imdb|tmdb)")
async def _imdb_search(e):
    if tapiKey is None:
        return await e.reply("IMDB API key is not set.")
    try:
        query = e.text.split(None, maxsplit=1)[1]
    except IndexError:
        return await e.reply("Provide the title name!")
    url = "https://api.themoviedb.org/3/search/multi"
    params = {
        "api_key": tapiKey,
        "query": quote(query),
        "language": "en-US",
        "page": "1",
        "include_adult": "false",
        "append_to_response": "credits,videos"
    }
    response = get(url, params=params, headers={
                   "User-Agent": "Mozilla/5.0"}, timeout=10).json()
    if response["results"]:
        result = response["results"][0]
        await e.reply('''
        **ID:** `{}`
        **Title:** {}
        **Release Date:** {}
        **Rating:** {}
        **Genres:** {}
        **Overview:** ```{}```
        **Popularity:** {}
        '''.format(result["id"], result["title"] if "title" in result else result["name"], result["release_date"], result["vote_average"],
                   ", ".join(result["genre_ids"]), result["overview"], result["popularity"]), parse_mode="md", link_preview=False, file="https://image.tmdb.org/t/p/w500" + result["poster_path"] if "poster_path" in result else None)
    else:
        await e.reply("No results found!")
