from urllib.parse import quote

from ._config import TMDB_KEY as tapiKey
from ._handler import newMsg

@newMsg(pattern="(imdb|tmdb)")
async def _imdb_search(e):
    try:
        query = e.text.split(None, maxsplit=1)[1]
    except IndexError:
        return await e.reply("Provide the title name!")
    url = "https://api.themoviedb.org/3/search/multi"
    params = {
        "api_key": tapiKey,
        "query": quote(query),
         "language":      "en-US",
	"page":          "1",
	"include_adult": "false",
    }
    # baaki naale
    print(url, params)
