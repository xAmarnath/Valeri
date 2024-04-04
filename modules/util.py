import os

from ._helpers import human_readable_size as hs

emoji_dict = {
    "📁": "folder",
    "📄": "file",
    "🎥": "video",
    "🎵": "audio",
    "🖼": "image",
    "🎇": "gif",
    "🗜": "archive",
    "📝": "text",
    "🐍": "python",
}


def get_emoji(file_name):
    file_ext = os.path.splitext(file_name)[1].lower()
    if file_ext in (".mp4", ".mkv", ".webm", ".3gp", ".mpeg"):
        return "🎥"
    elif file_ext in (".mp3", ".wav", ".flv", ".ogg", ".opus"):
        return "🎵"
    elif file_ext in (".jpg", ".jpeg", ".png", ".webp"):
        return "🖼"
    elif file_ext == ".gif":
        return "🎇"
    elif file_ext in (".zip", ".rar", ".7z", ".tar", ".gzip"):
        return "🗜"
    elif file_ext in (".json", ".xml", ".txt", ".text", ".csv", ".pptx", ".md"):
        return "📝"
    elif file_ext == ".py":
        return "🐍"
    else:
        return "📄"


def get_size(file_path):
    if os.path.isdir(file_path):
        size = 0
        for file_name in os.listdir(file_path):
            size += get_size(os.path.join(file_path, file_name))
        return hs(size)
    else:
        return hs(os.path.getsize(file_path))


def get_type(file_path):
    if os.path.isdir(file_path):
        return "folder"
    else:
        return emoji_dict[get_emoji(file_path)]


def get_name(file_path):
    if os.path.isdir(file_path):
        return os.path.basename(file_path)
    else:
        return os.path.basename(file_path)


def read_dir_to_string(dir_path):
    # read all files and folders in a directory and return a string
    # with all files and folders in a directory
    files = os.listdir(dir_path)
    files.sort()
    msg = "<b>Files in:</b> <code>{}</code>\n\n".format(dir_path)
    total_size = 0
    total_file_count = 0
    total_folder_count = 0
    for file_name in files:
        file_path = os.path.join(dir_path, file_name)
        msg += "{} <code>{}</code> <b>[{}]</b>".format(
            get_emoji(file_path), get_name(file_path), get_type(file_path)
        )
        if get_type(file_path) == "folder":
            msg += " <b>[{}]</b>".format(len(os.listdir(file_path)))
            total_folder_count += 1
        else:
            size = get_size(file_path)
            msg += " <b>[{}]</b>".format(size)
            total_size += size
            total_file_count += 1
        msg += "\n"
    msg += "\n<b>Total Size:</b> <code>{}</code>\n".format(total_size)
    msg += "<b>Total Files:</b> <code>{}</code>\n".format(total_file_count)
    msg += "<b>Total Folders:</b> <code>{}</code>\n".format(total_folder_count)
    return msg
