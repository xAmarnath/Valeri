import requests, json

cookies = {
    'tph_uuid': 'YqPsgPsRH4tB5rpzGTR7CGaGngwDHJpG8c8o2ygHAH',
}

from bs4 import BeautifulSoup

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    tags_data = []

    for element in soup.contents:
        if isinstance(element, str):
            tags_data.append({
                "tag": "p",
                "attrs": {"dir": "auto"},
                "children": [element]
            })
        else:
            tag_data = {
                "tag": element.name,
                "attrs": element.attrs,
                "children": []
            }

            tag_data["attrs"]["dir"] = "auto"

            if element.string:
                tag_data["children"].append(element.string)
            else:
                for child in element.contents:
                    if isinstance(child, str):
                        tag_data["children"].append(child)

            tags_data.append(tag_data)

    return tags_data


headers = {
    'authority': 'edit.legra.ph',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'multipart/form-data; boundary=---------------------------TelegraPhBoundary21',
    'origin': 'https://te.legra.ph',
    'referer': 'https://te.legra.ph/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
}

from ._handler import new_cmd

@new_cmd(pattern="(telegraph|tg|telegra\.ph) ?(.*)")
async def telegraph(e):
    if e.is_reply:
        text = (await e.get_reply_message()).message
    else:
        try:
            text = e.text.split(" ", 1)[1]
        except IndexError:
            return await e.edit("Give me some text to make telegraph link.")
    msg = await e.reply("Processing...")
    if len(text) == 0:
        return await e.edit("Give me some text to make telegraph link.")
    
    data = '-----------------------------TelegraPhBoundary21\r\nContent-Disposition: form-data; name="Data";filename="content.html"\r\nContent-type: plain/text\r\n\r\n{}\r\n-----------------------------TelegraPhBoundary21\r\nContent-Disposition: form-data; name="title"\r\n\r\n{}\r\n-----------------------------TelegraPhBoundary21\r\nContent-Disposition: form-data; name="author"\r\n\r\n\r\n-----------------------------TelegraPhBoundary21\r\nContent-Disposition: form-data; name="author_url"\r\n\r\n\r\n-----------------------------TelegraPhBoundary21\r\nContent-Disposition: form-data; name="save_hash"\r\n\r\n00620991d98291c5988be7f5535656ef2b16\r\n-----------------------------TelegraPhBoundary21\r\nContent-Disposition: form-data; name="page_id"\r\n\r\n0\r\n-----------------------------TelegraPhBoundary21--'.format(json.dumps(parse_html(text)), text[:20])
    response = requests.post('https://edit.legra.ph/save', cookies=cookies, headers=headers, data=data)

    if response.status_code == 200:
        await msg.edit(f"https://te.legra.ph/{response.json()['path']}")
    else:
        await msg.edit("Something went wrong. Please try again later.")


@new_cmd(pattern="(cupload|cup) ?(.*)")
async def c_upload(e):
    if not e.is_Reply:
        return await e.edit("Reply to a media to upload it to Cloud.")
    msg = await e.reply("Processing...")
    reply_ = await e.get_reply_message()
    if not reply_.media:
        return await msg.edit("Reply to a media to upload it to Cloud.")
    
    if reply_.file and reply_.file.size > 512 * 1024 * 1024: # 512 MB
        return await msg.edit("File size Limit is 512 MB.")
    
    _med = await reply_.download_media()
    if not _med:
        return await msg.edit("Something went wrong.")
    

    
    with open(_med, "rb") as f:
        data = f.read()
        resp = requests.post("https://envs.sh", files={"file": data})
        if resp.status_code == 200:
            await msg.edit(f"https://envs.sh/{resp.text}")
        else:
            await msg.edit("Something went wrong. Please try again later.")

        