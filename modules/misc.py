from urllib.parse import quote

from requests import get
from telethon import Button

from ._config import TMDB_KEY as tapiKey
from ._handler import newMsg
from ._helpers import human_currency


@newMsg(pattern="(imdb|tmdb)")
async def _imdb_search(e):
    if tapiKey is None:
        return await e.reply("IMDB API key is not set.")
    try:
        query = e.text.split(None, maxsplit=1)[1]
    except IndexError:
        return await e.reply("Provide the title name!")
    caption, url, buttons = search_imdb(query)
    if len(caption) > 1024:
        caption = caption[:1020] + "..."
    await e.reply(caption, file=url, parse_mode="html", buttons=buttons)


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
