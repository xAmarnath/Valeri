import random
import re
import sre_constants
from telethon import events, types
from ._config import bot
from .db import afk as db
from ._helpers import human_readable_time
from ._handler import newMsg

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


@bot.on(
    events.NewMessage(
        incoming=True,
    )
)
async def afk(e):
    if not e.from_id and not e.is_group and not e.sender:
        return
    if not isinstance(e.sender, types.User):
        return
    if (
        e.text
        and not len(e.text) in [0, 1]
        and (
            (e.text[1:].split()[0]).lower(
            ) == "afk" or e.text.lower().startswith("brb")
        )
    ):
        name = e.sender.first_name
        name = name + " " + e.sender.last_name if e.sender.last_name else name
        reason = (
            e.text.split(maxsplit=1)[1] if len(
                e.text.split(maxsplit=1)) == 2 else ""
        )
        await e.reply("{} is now afk.".format(name))
        return db.set_afk(e.sender_id, name, reason, True)
    elif db.is_afk(e.sender_id):
        c = db.get_afk(e.sender_id)
        name = e.sender.first_name
        name = name + " " + e.sender.last_name if e.sender.last_name else name
        await e.reply(random.choice(options).format(name, human_readable_time(c['time'])))
        db.set_afk(e.sender_id, "", "", False)
    else:
        c = await get_entities(e)
        if c and db.is_afk(c):
            c = db.get_afk(c)
            reason = "\n**Reason:** " + \
                c['reason'] if c['reason'] != "" else ""
            await e.reply(
                "**{}** has been afk since **{}**.{}".format(
                    c['name'], human_readable_time(c['time']), reason
                )
            )


async def get_entities(e):
    '''Gets the entities in the message.'''
    if e.reply_to_msg_id:
        r = await e.get_reply_message()
        try:
            return r.sender_id
        except AttributeError:
            return None
    else:
        try:
            for (x, y) in e.get_entities_text():
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


def infinite_checker(repl):
    regex = [
        r"\((.{1,}[\+\*]){1,}\)[\+\*].",
        r"[\(\[].{1,}\{\d(,)?\}[\)\]]\{\d(,)?\}",
        r"\(.{1,}\)\{.{1,}(,)?\}\(.*\)(\+|\* |\{.*\})",
    ]
    for match in regex:
        status = re.search(match, repl)
        return bool(status)


DELIMITERS = ("/", ":", "|", "_")


def seperate_sed(sed_string):
    if (
        len(sed_string) >= 3
        and sed_string[1] in DELIMITERS
        and sed_string.count(sed_string[1]) >= 2
    ):
        delim = sed_string[1]
        start = counter = 2
        while counter < len(sed_string):
            if sed_string[counter] == "\\":
                counter += 1

            elif sed_string[counter] == delim:
                replace = sed_string[start:counter]
                counter += 1
                start = counter
                break

            counter += 1

        else:
            return None
        while counter < len(sed_string):
            if (
                sed_string[counter] == "\\"
                and counter + 1 < len(sed_string)
                and sed_string[counter + 1] == delim
            ):
                sed_string = sed_string[:counter] + sed_string[counter + 1:]

            elif sed_string[counter] == delim:
                replace_with = sed_string[start:counter]
                counter += 1
                break

            counter += 1
        else:
            return replace, sed_string[start:], ""

        flags = ""
        if counter < len(sed_string):
            flags = sed_string[counter:]
        return replace, replace_with, flags.lower()


@newMsg(pattern=r"^s([/:|_]).*?\1.*")
async def reg_x__se_dd(e):
    if not e.text:
        return
    if e.reply_to_msg_id:
        r = await e.get_reply_message()
        if not r.text:
            return
        fix = r.text
        try:
            x, y, z = seperate_sed(e.text)
        except:
            return
        if not x:
            return await e.reply(
                "You're trying to replace... " "nothing with something?"
            )
        try:
            if infinite_checker(x):
                return await e.reply("Nice try -_-")

            if "i" in z and "g" in z:
                text = re.sub(x, y, fix, flags=re.I).strip()
            elif "i" in z:
                text = re.sub(x, y, fix, count=1, flags=re.I).strip()
            elif "g" in z:
                text = re.sub(x, y, fix).strip()
            else:
                text = re.sub(x, y, fix, count=1).strip()
        except sre_constants.error as xc:
            return await e.reply(str(xc))
        if len(text) >= 4096:
            await e.reply(
                "The result of the sed command was too long for \
                                                 telegram!"
            )
        elif text:
            await e.respond(text, reply_to=e.reply_to_msg_id or e.id)
