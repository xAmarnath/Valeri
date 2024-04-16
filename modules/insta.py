from ._handler import new_cmd


@new_cmd(pattern="(insta|instagram|instadl|instadownload)")
async def _insta(message):
    # TODO: implement

    await message.reply("This feature is not implemented yet.")
