from telethon import errors, functions, types

from ._handler import newMsg
from ._helpers import get_mention, get_user, has_admin_rights, parse_time


@newMsg(pattern="(promote|superpromote|demote)")
async def promote_demote(e):
    action = e.text.split(" ")[0][1:].lower()
    r, arg = await has_admin_rights(e.chat_id, e.sender_id, "add_admins")
    if not r:
        return await e.reply(arg)
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
            await e.reply(f"Demoted {get_mention(user)}!")
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


@newMsg(pattern="(ban|kick|unban|tban|sban|mute|tmute|smute|skick|unmute|kickme)")
async def restrict_user(msg):
    action = msg.text.split(" ")[0][1:].lower()
    if action == "kickme":
        try:
            await msg.client.kick_participant(msg.chat_id, msg.from_id)
            await msg.reply("I have kicked you!")
        except Exception as ex:
            await msg.reply(str(ex) + str(type(ex)))
    r, arg = await has_admin_rights(msg.chat_id, msg.sender_id, "ban_users")
    if not r:
        return await msg.reply(arg)
    
    user, arg = await get_user(msg)
    if not user:
        return
    try:
        p = await msg.client(functions.channels.GetParticipantRequest(msg.chat_id, user.id))
        try:
          p.participant.admin_rights
          return await msg.reply("Sorry, can't restrict admins!")
        except AttributeError:
          pass
    except:
        pass
    if action in ["ban", "sban", "tban", "unban"]:
        if arg == "" and action == "tban":
            await msg.reply("Please specify a time!")
            return
        _time = parse_time(arg) if action == "tban" else None
        ban_rights = (
            types.ChatBannedRights(
                until_date=_time,
                view_messages=True,
            )
            if action in ["ban", "tban"]
            else types.ChatBannedRights(
                view_messages=True,
                until_date=None,
            )
        )
        ban_rights = (
            types.ChatBannedRights(
                view_messages=False,
                until_date=None,
            )
            if action == "unban"
            else ban_rights
        )
        try:
            await msg.client(
                functions.channels.EditBannedRequest(
                    msg.chat_id,
                    user.id,
                    banned_rights=ban_rights,
                )
            )
            if action != "sban":
                await msg.reply(
                    "Another one bites the dust! banned {}".format(get_mention(user))
                    if action in ["ban", "tban"]
                    else "Unbanned!, {} is now free to chat".format(get_mention(user))
                )
        except errors.rpcerrorlist.UserAdminInvalidError:
            await msg.reply(
                "I can't do this to this user!, make sure I have ban rights to the chat"
            )
        except errors.rpcerrorlist.UserIdInvalidError:
            await msg.reply("I can't find this user!")
        except errors.rpcerrorlist.UserNotMutualContactError:
            await msg.reply("This user is not in your contact list!")
        except errors.rpcerrorlist.UserAlreadyParticipantError:
            await msg.reply("This user is already in the chat!")
        except errors.rpcerrorlist.UserCreatorError:
            await msg.reply(
                "I would love to ban the chat creator, but... not in the mood to do so."
            )
        except Exception as ex:
            await msg.reply(str(ex) + str(type(ex)))
    elif action in ["mute", "tmute", "smute", "unmute"]:
        if arg == "" and action == "tban":
            await msg.reply("Please specify a time!")
            return
        _time = parse_time(arg) if action == "tmute" else None
        mute_rights = (
            types.ChatBannedRights(
                until_date=_time,
                send_messages=True,
            )
            if action in ["mute", "smute"]
            else types.ChatBannedRights(
                send_messages=True,
                until_date=None,
            )
        )
        mute_rights = (
            types.ChatBannedRights(send_messages=False, until_date=None)
            if action == "unmute"
            else mute_rights
        )
        try:
            await msg.client(
                functions.channels.EditBannedRequest(
                    msg.chat_id,
                    user.id,
                    banned_rights=mute_rights,
                )
            )
            if action != "smute":
                await msg.reply(
                    "Muted {}!".format(get_mention(user))
                    if action in ["mute", "tmute"]
                    else "Unmuted!, {} is now free to talk".format(get_mention(user))
                )
        except errors.rpcerrorlist.UserAdminInvalidError:
            await msg.reply(
                "I can't do this to this user!, make sure I have ban rights to the chat"
            )
        except errors.rpcerrorlist.UserIdInvalidError:
            await msg.reply("I can't find this user!")
        except errors.rpcerrorlist.UserNotMutualContactError:
            await msg.reply("This user is not in your contact list!")
        except errors.rpcerrorlist.UserAlreadyParticipantError:
            await msg.reply("This user is already in the chat!")
        except errors.rpcerrorlist.UserCreatorError:
            await msg.reply(
                "I would love to mute the chat creator, but... its impossible."
            )
        except Exception as ex:
            await msg.reply(str(ex) + str(type(ex)))
    elif action in ["kick", "skick"]:
        try:
            await msg.client.kick_participant(msg.chat_id, user.id)
            if action != "skick":
                await msg.reply("I have kicked {}!".format(get_mention(user)))
        except errors.rpcerrorlist.UserAdminInvalidError:
            await msg.reply(
                "I can't do this to this user!, make sure I have ban rights to the chat"
            )
        except errors.rpcerrorlist.UserIdInvalidError:
            await msg.reply("I can't find this user!")
        except errors.rpcerrorlist.UserNotMutualContactError:
            await msg.reply("This user is not in your contact list!")
        except errors.rpcerrorlist.UserAlreadyParticipantError:
            await msg.reply("This user is already in the chat!")
        except errors.rpcerrorlist.UserCreatorError:
            await msg.reply(
                "I would love to kick the chat creator, but... not in the mood to do so."
            )
        except Exception as ex:
            await msg.reply(str(ex) + str(type(ex)))
