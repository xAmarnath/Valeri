from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import (
    UpdateBotMessageReaction,
    UpdateBotMessageReactions,
    ReactionEmoji,
)
from telethon import events
import re

from ._handler import new_cmd
from ._config import bot
from .db.db import DB as db
db = db.react


react_filter_cache = {}

def add_reaction_filter(msg_id, filter_word, reaction, sender_id, chat_id):
    db.update_one(
        {"msg_id": msg_id},
        {
            "$set": {
                "msg_id": msg_id,
                "filter_word": filter_word,
                "reaction": reaction,
                "sender_id": sender_id,
                "chat_id": chat_id,
            }
        },
        upsert=True,
    )

    react_filter_cache[msg_id] = [filter_word, reaction, sender_id, True, chat_id]


def remove_reaction_filter(chat_id, word) -> bool:
    db.delete_one({"chat_id": chat_id, "filter_word": word})
    for msg_id, data in react_filter_cache.copy().items():
        if data[0] == word and data[4] == chat_id:
            del react_filter_cache[msg_id]
            return True
    return False


def _load_db_cache():
    try:
        for data in db.find({}):
            react_filter_cache[data["msg_id"]] = [
                data["filter_word"],
                data["reaction"],
                data["sender_id"],
                True,
                data["chat_id"],
            ]
    except Exception as e:
        print("Error loading reaction filter cache", e)


_load_db_cache()
print("Loaded reaction filter cache successfully!: ", react_filter_cache)


@new_cmd(pattern=r"rf(?: |$)(.*)")
async def react_filter(e):
    if e.is_reply:
        r = await e.get_reply_message()
        if r.media:
            if r.photo:
                filter_word = r.photo.id
            elif r.document:
                filter_word = r.document.id
            else:
                return await e.reply("**I can only filter media/text messages!**")
        else:
            filter_word = r.text
    else:
        try:
            filter_word = e.text.split(" ", maxsplit=1)[1]
        except IndexError:
            return await e.reply("Usage: `/rf <word>`")
    msg = await e.reply("**React to the message you want to set as reaction filter.**")
    react_filter_cache[msg.id] = [filter_word, "", e.sender_id, False, e.chat_id]

@new_cmd(pattern=r"rrf(?: |$)(.*)")
async def react_remove_filter(e):
    if e.is_reply:
        r = await e.get_reply_message()
        if r.media:
            if r.photo:
                filter_word = r.photo.id
            elif r.document:
                filter_word = r.document.id
        else:
            filter_word = r.text
    else:
        try:
            filter_word = e.text.split(" ", maxsplit=1)[1]
        except IndexError:
            return await e.reply("Usage: `/rrf <word>`")
    if remove_reaction_filter(e.chat_id, filter_word):
        await e.reply(f"**Removed filter `{filter_word}` successfully!**")
    else:
        await e.reply(f"**No such filter found!**")


@bot.on(events.NewMessage)
async def reaction_filter_trigger(e):
    for _, data in react_filter_cache.copy().items():
        if e.chat_id == data[4] and (re.search("\b" + str(data[0]) + "\b", e.text, re.IGNORECASE) or (e.photo and data[0] == e.photo.id) or (e.document and data[0] == e.document.id)):
            if data[1] == "":
                return
            await bot(
                SendReactionRequest(
                    await bot.get_input_entity(e.chat_id),
                    e.id,
                    True,
                    False,
                    [ReactionEmoji(data[1])],
                )
            )
            return


@bot.on(events.Raw([UpdateBotMessageReactions, UpdateBotMessageReaction]))
async def reaction_handler(e):
    if isinstance(e, UpdateBotMessageReaction):
        msg_id = e.msg_id
        if (
            msg_id in react_filter_cache
            and (await bot.get_peer_id(e.actor)) == react_filter_cache[msg_id][2]
            and not react_filter_cache[msg_id][3]
        ):
            react_filter_cache[msg_id][1] = e.new_reactions[0].emoticon
            message = await bot.get_messages(e.peer, ids=msg_id)
            await message.edit(f"**Filter set Successfully!**")
            react_filter_cache[msg_id][3] = True
            add_reaction_filter(
                msg_id,
                react_filter_cache[msg_id][0],
                react_filter_cache[msg_id][1],
                react_filter_cache[msg_id][2],
                react_filter_cache[msg_id][4],
            )


def get_new_appeared_reaction(old_reactions, new_reactions):
    try:
        for new_reaction in new_reactions.reverse():
            if new_reaction not in old_reactions:
                return new_reaction
    except AttributeError:
        return None
    
@new_cmd(pattern=r"reactions(?: |$)(.*)")
async def get_reactions(e):
    current_chat_reaction_filters = []
    for _, data in react_filter_cache.copy().items():
        if e.chat_id == data[4]:
            current_chat_reaction_filters.append(data)
    if not current_chat_reaction_filters:
        return await e.reply("**No reaction filters in this chat!**")
    await e.reply(
        "**Current reaction filters in this chat:**\n\n"
        + "\n".join(
            [
                f"**{x[0]}** - `({x[1]})`"
                for x in current_chat_reaction_filters
            ]
        )
    )
