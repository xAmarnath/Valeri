import asyncio
from os import remove, rename

from PIL import Image
from requests import get, post

from ._handler import newMsg


async def run_cmd(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    o, e = await proc.communicate()
    return str(o), str(e)


def color_image(path):
    with open(path, "rb") as file:
        r = post(
            "https://api.deepai.org/api/colorizer",
            files={"image": file},
            headers={"api-key": "quickstart-QUdJIGlzIGNvbWluZy4uLi4K"},
        )
        with open("color-" + path, "wb") as file:
            data = r.json()
            try:
                url = data["output_url"]
            except KeyError:
                return "", str(data)
            file.write(get(url).content)
    return "color-" + path, ""


def similarize_image(image):
    image1 = Image.open(image)
    image2 = Image.open("color-" + image)
    image2 = image2.resize((image1.size[0], image1.size[1]))
    image2.save("color-" + image)


FFMPEG_COMMAND = 'ffmpeg -loop 1 -framerate 30 -t 0.16 -i {}  -loop 1 -framerate 30 -t 0.16 -i {} -loop 1 -framerate 30 -t 0.16 -i {} -loop 1 -framerate 30 -t 0.16 -i {} -filter_complex "[0][1][2][3]concat=n=4:v=1:a=0[v1],[v1]loop=20:32767:0" {}'


@newMsg(pattern="animate")
async def _animate(msg):
    if not msg.reply_to:
        return await msg.reply("Reply to sticker/photo to animate it")
    r = await msg.get_reply_message()
    mg = await msg.reply("`Processing..`")
    if not any([r.photo, r.sticker]):
        return await msg.reply("nil")
    f = await r.download_media()
    color_f, err = color_image(f)
    if err != "":
        return await mg.edit(str(err))
    similarize_image(f)
    await run_cmd(
        FFMPEG_COMMAND.format(f, color_f, f, color_f, "{}-anim.mp4".format(msg.id))
    )
    await msg.respond(file="{}-anim.mp4".format(msg.id))
    await mg.delete()


@newMsg(pattern="color")
async def _animate(msg):
    if not msg.reply_to:
        return await msg.reply("Reply to sticker/photo to animate it")
    r = await msg.get_reply_message()
    mg = await msg.reply("`Processing..`")
    if not any([r.photo, r.sticker]):
        return await msg.reply("nil")
    f = await r.download_media()
    color_f, err = color_image(f)
    if err != "":
        return await mg.edit(str(err))
    await msg.respond(file=color_f)
    await mg.delete()


@newMsg(pattern="(stoi|itos)")
async def _stoi(message):
    if not message.reply_to:
        return await message.reply("Reply to a media to convert it to sticker.")
    r = await message.get_reply_message()
    if not r.media:
        return await message.reply("Reply to a media to convert it to sticker.")
    if not any([r.photo, r.sticker]):
        return await message.reply("Reply to a media to convert it to sticker.")
    media = await r.download_media()
    if "stoi" in message.text:
        rename(media, media + ".png")
        media += ".png"
    else:
        rename(media, media + ".webp")
        media += ".webp"
    await message.respond(file=media)
    remove(media)
    remove(media.replace("." + media.split(".")[-1], ""))
