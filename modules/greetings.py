from telethon import events, types
from ._config import bot
from .db import greet as db


@bot.on(
    events.Raw(
        types.UpdateChannelParticipant,
        func=lambda e: not e.prev_participant
        and e.new_participant
        and not isinstance(
            e.new_participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantBanned),
        )
        and not int("-100" + str(e.channel_id)) in db.welcome_blacklist,
    )
)
async def welcome(e):
    print(e)
