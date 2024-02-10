from ._handler import newIn
from telethon import Button, events
from ._config import bot

whisper_db = []


@newIn(pattern="wh (.*?)")
async def _inline_whisper(e: events.InlineQuery.Event):
    try:
        payload = e.text[len("wh ") :]
        entity = payload.split(" ")[0].strip()
        text = payload.split(" ", maxsplit=2)[1].strip()

        if entity.startswith("@") or entity.isalnum():
            try:
                user = await e.client.get_entity(entity)
            except ValueError:
                return await e.answer(
                    [
                        await e.builder.article(
                            title="User not found!",
                            description="User not found!",
                            text="User not found!",
                            buttons=[Button.switch_inline("Try Again", "wh ", True)],
                        )
                    ]
                )
            user_id = user.id
            user_name = user.username
        elif entity.isdigit():
            user_id = int(entity)
            user_name = "Unknown({})".format(user_id)
        else:
            return await e.answer(
                [
                    await e.builder.article(
                        title="Invalid Username!",
                        description="Invalid Username!",
                        text="Invalid Username!",
                        buttons=[Button.switch_inline("Try Again", "wh ", True)],
                    )
                ]
            )

        if user_id == e.sender_id:
            return await e.answer(
                [
                    await e.builder.article(
                        title="You can't whisper yourself!",
                        description="You can't whisper yourself!",
                        text="You can't whisper yourself!",
                        buttons=[Button.switch_inline("Try Again", "wh ", True)],
                    )
                ]
            )

        whisper_db.append((user_id, user_name, text, e.id))
        whisper_emoji = "📩"
        print(whisper_db)

        return await e.answer(
            [
                await e.builder.article(
                    title="Whisper Sent To {}".format(user_name),
                    description="Whisper Sent!",
                    text="Click to open the whisper Message, (Only for {})\n\n{}".format(
                        user_name, whisper_emoji
                    ),
                    buttons=[
                        Button.inline(
                            "Open {}".format(whisper_emoji),
                            data="whisper_{}".format(e.id),
                        )
                    ],
                )
            ]
        )

    except IndexError:
        await e.answer(
            [
                await e.builder.article(
                    title="Usage: @username text",
                    description="Usage: @username text",
                    text="Whisper Usage: @username text",
                    buttons=[Button.switch_inline("Try Again", "wh ", True)],
                )
            ]
        )

@bot.on(events.CallbackQuery(pattern=r"whisper_(.*)"))
async def _whisper_open(e: events.CallbackQuery.Event):
    print(whisper_db)
    try:
        query_id = int(e.data.decode().split("_")[1])
        for user_id, user_name, text, id in whisper_db:
            if id == query_id:
                await e.answer(text, alert=True)
                await e.edit(f"Whisper Already Opened.")
                del whisper_db[whisper_db.index((user_id, user_name, text, id))]
                break
    except Exception as e:
        await e.answer("Error: {}".format(e), alert=True)