from .db.db import DB, DB_MODE

if DB_MODE == "mongo":
    afk = DB.afk
else:
    afk = DB

import random
import time

from telethon import events, types

from ._config import bot


def set_afk(user_id, name, reason, state, file: list = None):
    if state:
        if DB_MODE == "sql":
            afk.execute(
                "INSERT INTO afk (user_id, name, reason, state, time, file) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, name, reason, state, time.time(), file if file else []),
            )
        else:
            afk.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "user_id": user_id,
                        "name": name,
                        "reason": reason,
                        "state": state,
                        "time": time.time(),
                        "file": file if file else [],
                    }
                },
                upsert=True,
            )
        AFK_CACHE.append(user_id)
    else:
        if DB_MODE == "sql":
            afk.execute("DELETE FROM afk WHERE user_id = ?", (user_id,))
        else:
            afk.delete_one({"user_id": user_id})
        if user_id in AFK_CACHE:
            AFK_CACHE.remove(user_id)


AFK_CACHE = []


def is_afk(user_id):
    if user_id in AFK_CACHE:
        return True
    return False


def get_afk(user_id):
    return afk.find_one({"user_id": user_id})


def __load_cached_Afk():
    try:
        if DB_MODE == "sql":
            # if table afk does not exist, create it
            afk.execute(
                "CREATE TABLE IF NOT EXISTS afk (user_id INTEGER PRIMARY KEY, name TEXT, reason TEXT, state BOOLEAN, time INTEGER, file TEXT)"
            )
            for data in afk.execute("SELECT user_id FROM afk"):
                AFK_CACHE.append(data[0])
        else:
            for data in afk.find({}):
                AFK_CACHE.append(data["user_id"])
    except Exception as e:
        print("Error loading afk cache", e)


options = [
    "**{}** is here, was afk for {}",
    "**{}** is back, been away for {}",
    "**{}** is now in the chat!, back after {}",
    "**{}** is awake, was afk for {}",
    "**{}** is back online, away for {}",
    "**{}** is finally here, was afk for {}",
    "Welcome back! **{}**, was afk for {}",
    "Where is **{}**?\nIn the chat!, was away for {}",
    "Pro **{}**, is back alive!, after {}",
]


def convert_dt(seconds: int) -> str:
    seconds = time.time() - seconds
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


@bot.on(events.NewMessage(pattern=r"(.*)"))
async def _xafk(e):
    if not e.from_id and not e.is_group and not e.sender:
        return
    if not isinstance(e.sender, types.User):
        return
    if (
        e.text
        and not len(e.text) in [0, 1]
        and (
            (e.text[1:].split()[0]).lower() == "afk" or e.text.lower().startswith("brb")
        )
    ):
        name = e.sender.first_name
        name = name + " " + e.sender.last_name if e.sender.last_name else name
        reason = (
            e.text.split(maxsplit=1)[1] if len(e.text.split(maxsplit=1)) == 2 else ""
        )
        if e.is_reply:
            r = await e.get_reply_message()
            if r.media:
                if r.photo:
                    file = [r.photo.id, r.photo.access_hash, 1]
                elif r.sticker:
                    file = [r.sticker.id, r.sticker.access_hash, 2]
                elif r.document:
                    file = [r.document.id, r.document.access_hash, 0]
                else:
                    file = []
            else:
                file = []
        else:
            file = []
        await e.reply("{} is now afk.".format(name))
        return set_afk(e.sender_id, name, reason, True, file)
    elif is_afk(e.sender_id):
        c = get_afk(e.sender_id)
        name = e.sender.first_name
        name = name + " " + e.sender.last_name if e.sender.last_name else name
        await e.reply(random.choice(options).format(name, convert_dt(c["time"])))
        set_afk(e.sender_id, "", "", False)
    else:
        c = await get_entities(e)
        if c and is_afk(c):
            c = get_afk(c)
            reason = "\n**Reason:** " + c.get("reason") if c.get("reason") else ""
            if c.get("file", None):
                if len(c["file"]) == 3:
                    if c["file"][2] == 1:
                        file = types.InputPhoto(c["file"][0], c["file"][1], b"")
                    else:
                        file = types.InputDocument(c["file"][0], c["file"][1], b"")
                    if c.get("file")[2] == 2:
                        await e.reply(
                            file=file,
                        )
                        await e.reply(
                            "**{}** has been afk since **{}**.{}".format(
                                c.get("name"), convert_dt(c.get("time")), reason
                            ),
                        )
                        return
                    await e.reply(
                        "**{}** has been afk since **{}**.{}".format(
                            c.get("name"), convert_dt(c.get("time")), reason
                        ),
                        file=file,
                    )
                    return

            await e.reply(
                "**{}** has been afk since **{}**.{}".format(
                    c.get("name"), convert_dt(c.get("time")), reason
                ),
            )


async def get_entities(e):
    if e.reply_to_msg_id:
        r = await e.get_reply_message()
        try:
            return r.sender_id
        except AttributeError:
            return None
    else:
        try:
            for x, y in e.get_entities_text():
                if x.offset != 0:
                    break
                elif isinstance(x, types.MessageEntityMention):
                    pass
                elif isinstance(x, types.MessageEntityMentionName):
                    pass
                else:
                    return None
                return y.split()[0]
        except:
            return None


__load_cached_Afk()
