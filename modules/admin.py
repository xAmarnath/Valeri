from telethon import errors, functions, types

from ._handler import newMsg
from ._helpers import get_mention, get_user


@newMsg(pattern="(promote|superpromote|demote)")
async def _promote_demote(e):
    action = e.text.split(" ")[0][1:]
    user, arg = await get_user(e)
    if not user:
        return
    try:
        if action == "promote":
            await e.client(
                functions.channels.EditAdminRequest(
                    e.chat_id,
                    user.id,
                    admin_rights=types.ChatAdminRights(
                        delete_messages=True,
                        ban_users=True,
                        invite_users=True,
                        pin_messages=True,
                    ),
                    rank=arg if arg else "Admin",
                )
            )
            await e.reply(
                get_mention(user) + " has been promoted to " + (arg or "Admin") + "."
            )
        elif action == "superpromote":
            await e.client(
                functions.channels.EditAdminRequest(
                    e.chat_id,
                    user.id,
                    admin_rights=types.ChatAdminRights(
                        add_admins=True,
                        delete_messages=True,
                        ban_users=True,
                        invite_users=True,
                        pin_messages=True,
                        manage_call=True,
                        change_info=True,
                    ),
                    rank=arg if arg else "SuperAdmin",
                )
            )
            await e.reply("Successfully superpromoted {}".format(get_mention(user)))
        elif action == "demote":
            await e.client(
                functions.channels.EditAdminRequest(
                    e.chat_id,
                    user.id,
                    admin_rights=types.ChatAdminRights(
                        delete_messages=False,
                        ban_users=False,
                        invite_users=False,
                        pin_messages=False,
                        manage_call=False,
                        change_info=False,
                    ),
                    rank=arg if arg else "Member",
                )
            )
            await e.reply("Demoted {}!".format(get_mention(user)))
    except errors.ChatAdminRequiredError:
        await e.reply("Failure!, make sure I have add admin rights to the chat")
    except errors.rpcerrorlist.UserCreatorError:
        await e.reply(
            "I would love to promote the chat creator, but... well, they already have all the power."
        )
    except errors.rpcerrorlist.BotChannelsNaError:
        await e.reply("Due to telegram restrictions, I can't demote bots.")
    except errors.UserAdminInvalidError:
        await e.reply("I can't do this to this user!")
    except errors.UserIdInvalidError:
        await e.reply("I can't find this user!")
    except errors.UserNotMutualContactError:
        await e.reply("This user is not in your contact list!")
    except errors.UserAlreadyParticipantError:
        await e.reply("This user is already in the chat!")
    except Exception as ex:
        await e.reply(str(ex) + str(type(ex)))
