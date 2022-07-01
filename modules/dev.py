from ._handler import newMsg, auth_only
from os import listdir, path
from ._helpers import human_readable_size


@newMsg(pattern="ls")
@auth_only
async def _ls(e):
    try:
        directory = e.text.split(" ", 1)[1]
    except IndexError:
        directory = "./"
    contents = listdir(directory)
    if len(contents) == 0:
        await e.reply("`No files found.`")
        return
    caption = "`Files in {}:`\n".format(directory)
    folder_count = 0
    file_count = 0
    for file in contents:
        size = path.getsize(directory + file)
        if path.isdir(directory + file):
            folder_count += 1
            caption += "📁 <code>{}</code> (<code>{}</code>)\n".format(
                file, human_readable_size(size))
        else:
            file_count += 1
            if file.endswith(".mp4") or file.endswith(".mkv") or file.endswith(".webm"):
                emoji = "🎥"
            elif file.endswith(".mp3") or file.endswith(".wav"):
                emoji = "🎵"
            elif file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
                emoji = "🖼"
            elif file.endswith(".gif"):
                emoji = "🎇"
            elif file.endswith(".zip") or file.endswith(".rar") or file.endswith(".7z"):
                emoji = "🗜"
            else:
                emoji = "📄"
            caption += "{} <code>{}</code> (<code>{}</code>)\n".format(emoji,
                                                                       file, human_readable_size(size))
    caption += "\n`{} folders, {} files`".format(folder_count, file_count)
    await e.reply(caption, parse_mode="html")
