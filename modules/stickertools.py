from os import remove, rename

from ._handler import newMsg
from requests import post , get
import asyncio
from PIL import Image

async def run_cmd(cmd):
 proc = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
 o, e = await proc.communicate()
 return str(o), str(e)

def color_image(path):
    with open(path, 'rb') as file
     r = post('https://api.deepai.org/api/colorizer', files={"image": file}, headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'})
    with open('color-' + path, 'wb') as file:
      file.write(get(r.json()['output_url']))
    return 'color-' + path

def similarize_image(image):
    image1 = Image.open(image)
    image2 = Image.open('color-' + image)
    image2 = image2.resize((image1.size[0], image1.size[1]))
    image2.save('color-' + image)

FFMPEG_COMMAND = 'ffmpeg -loop 1 -framerate 30 -t 0.16 -i {}  -loop 1 -framerate 30 -t 0.16 -i {} -loop 1 -framerate 30 -t 0.16 -i {} -loop 1 -framerate 30 -t 0.16 -i {} -filter_complex "[0][1][2][3]concat=n=4:v=1:a=0[v1],[v1]loop=20:32767:0" {}'

@newMsg(pattern='animate')
async def _animate(msg):
 if not msg.reply_to:
    return await e.reply("Reply to sticker/photo to animate it")
 r = await msg.get_reply_message()
 mg = await msg.reply('`Processing..`')
 if not any([r.photo, r.sticker]):
    return await e.reply('nil')
 f = await r.download_media()
 color_f = color_image(f)
 similarize_image(f)
 await run_cmd(FFMPEG_COMMAND.format(f, color_f, f, color_f, '{}-anim.mp4'.format(msg.id)))
 await e.respond(file='{}-anim.mp4'.format(msg.id))
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
