from pyppeteer import launch
import asyncio

import time
import warnings
from urllib.parse import quote
import platform

from ._handler import new_cmd
from ._helpers import get_text_content

@new_cmd(pattern="(teradl|terabox)")
async def _terabox(message):
    try:
        url = await get_text_content(message)
    except Exception as e:
        return await message.reply(str(e))
    
    msg = await message.reply("Processing...")
    
    try:
        link, time_taken = await fetch_terrabox(url)
    except Exception as e:
        return await message.reply(str(e))
    
    msg = await msg.edit(f"Link: {link}\nTime taken: {time_taken} seconds")


warnings.filterwarnings("ignore")

local_override_chunk_name = "page-a90198bf7622b0294.js"

get_url = "https://teradownloader.com/download?link=https%3A%2F%2Fwww.terabox.app%2Fsharing%2Flink%3Fsurl%3DwQ3SJAY-DAaPfHEUduj-oA"


async def fetch_terrabox(url):
    final_url = "https://teradownloader.com/download?link=" + quote(url)
    
    if platform.system() == "Windows":
        browser = await launch({
            "executablePath": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "headless": False,
        })
    else:
        browser = await launch({
            "headless": True,
        })

    page = (await browser.pages())[0]

    t = time.time()
    await page.setRequestInterception(True)

    @page.on("request")
    def request_interception(req):
            # deny irrelevant requests
            if any(x in req.url for x in [".ttf", ".svg", ".jpg", ".css", ".webmanifest", ".png", ".ico", "ads"]):
                asyncio.ensure_future(req.abort())
            else:
                asyncio.ensure_future(req.continue_())

    await page.goto(final_url)
    
    # wait till https://d.terabox.app link appears in html content
    
    await page.waitForSelector("a[href^='https://d.terabox.app']", {"timeout": 40000})
    
    # take the link
    link = await page.evaluate("() => document.querySelector('a[href^=\"https://d.terabox.app\"]').href")
    
    browser.close()
    
    print("Link:", link)
    
    return link, time.time() - t
    
    # with open("test.html", "wb") as f:
    #     f.write((await page.content()).encode("utf-8"))

    # await page.waitForSelector("pre")
    # data = await page.evaluate("() => document.querySelector('pre').innerText")

    # print("ENC DATA:", data)
    
    # async with aiohttp.ClientSession() as session:
    #     async with session.get("https://teradownloader.com/api", params={"data": data}) as response:
    #         print((await response.json())[0]["dlink"])
            
    #         print("Time taken:", time.time() - t, "seconds")
    

    

# asyncio.get_event_loop().run_until_complete(fetch_terrabox("https://www.terabox.com/wap/share/filelist?surl=mxWuT1VZVsMdfi_Y0o5bgQ"))
