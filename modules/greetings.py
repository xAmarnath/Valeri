from telethon import events, types

from ._config import bot
from .db import greet as db
from .db.stats_db import add_chat


@bot.on(
    events.Raw(
        types.UpdateChannelParticipant,
        func=lambda e: not e.prev_participant
        and e.new_participant
        and not isinstance(
            e.new_participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantBanned),
        )
    )
)
async def welcome(e):
    add_chat(int("-100{}".format(e.channel_id)))
    
