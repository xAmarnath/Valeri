from ._handler import newMsg
from ._config import TMDB_KEY as apiKey
from urllib.parse import quote 

IMDB_BASE_URL = 'https://api.themoviedb.org/3'

@newMsg(pattern='(imdb|tmdb)')
async def _imdb_search(e):
 try:
  query = e.text.split(None, maxsplit=1)[1]
 except IndexError:
  return await e.reply("Provide the title name!")
 url = IMDB_BASE_URL + '/search/multi'
 params = {
 "api_key": apiKey
 "query": quote(query)
 }
 # baaki naale
 print(url, params)
