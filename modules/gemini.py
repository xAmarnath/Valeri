import base64
import os

from requests import post

from ._handler import new_cmd

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def send_prompt(prompt):
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key="
        + GEMINI_API_KEY
    )
    response = post(url, json={"contents": [{"parts": [{"text": prompt}]}]})

    if response.status_code != 200:
        return "Error: " + response.text

    gemini_response = response.json()
    final_text = ""
    for part in gemini_response["candidates"]:
        for t in part["content"]["parts"]:
            final_text += t["text"]
    return final_text


def resize_to_512_without_lose_aspect_ratio(image):
    h, w = image.size
    new_h = 512
    new_w = int(new_h * w / h)

    return image.resize((new_w, new_h))


def send_image_prompt(prompt, image):
    from PIL import Image

    im = resize_to_512_without_lose_aspect_ratio(Image.open(image))
    im.save(image, "JPEG")

    with open(image, "rb") as f:
        base_64 = base64.b64encode(f.read())

    with open("base64.txt", "wb") as f:
        f.write(base_64)

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key="
        + GEMINI_API_KEY
    )

    x = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": base_64.decode("utf-8"),
                        }
                    },
                ]
            }
        ]
    }

    response = post(
        url,
        json=x,
    )

    if response.status_code != 200:
        return "Error: " + response.text

    gemini_response = response.json()
    final_text = ""
    for part in gemini_response["candidates"]:
        for t in part["content"]["parts"]:
            final_text += t["text"]

    return final_text


if GEMINI_API_KEY:

    @new_cmd(pattern="gem (.*)")
    async def _(e):
        if e.fwd_from:
            return

        if e.reply_to_msg_id:
            r = await e.get_reply_message()
            if r.media:
                if r.document:
                    if r.media.document.mime_type == "image/jpeg":
                        await e.reply(
                            send_image_prompt(
                                e.pattern_match.group(1), await r.download_media()
                            ).strip()
                        )
                        return
                if r.photo:
                    await e.reply(
                        send_image_prompt(
                            e.pattern_match.group(1), await r.download_media()
                        ).strip()
                    )
                    return
            else:
                try:
                    et = e.text.split(" ", 1)[1]
                except:
                    et = ""
                await e.reply(send_prompt(et + " " + r.text).strip())
                return

        try:
            et = e.text.split(" ", 1)[1]
        except:
            await e.reply("Give me a prompt")
            return

        await e.reply(send_prompt(et).strip())
        return
