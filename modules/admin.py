from telethon import errors, functions, types

from ._handler import new_cmd
from ._helpers import (
    get_mention,
    get_text_content,
    get_user,
    has_admin_rights,
    parse_time,
)


@new_cmd(pattern="promote|superpromote|demote")
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
            await e.reply(get_mention(user) + " has been promoted!")
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
            await e.reply(get_mention(user) + " has been superpromoted!")
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


@new_cmd(pattern="ban|kick|unban|tban|sban|mute|tmute|smute|skick|unmute|kickme")
async def restrict_user(msg):
    action = msg.text.split(" ")[0][1:].lower() if not msg.text.startswith("/") else msg.text.split(" ")[0].lower()
    if action == "kickme":
        try:
            await msg.client.kick_participant(msg.chat_id, msg.from_id)
            return await msg.reply("I have kicked you!")
        except Exception:
            return await msg.reply("Unable to kick you.")
    r, arg = await has_admin_rights(msg.chat_id, msg.sender_id, "ban_users")
    if not r:
        return await msg.reply(arg)
    user, arg = await get_user(msg)
    if not user:
        return
    #try:
        #p = await msg.client(
            #functions.channels.GetParticipantRequest(msg.chat_id, user.id)
        #)
        #try:
           # p.participant.admin_rights
           # return await msg.reply("Sorry, can't restrict admins!")
        #except AttributeError:
           # pass
    #except:
        #pass
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


@new_cmd(pattern="chatid")
async def chatid(msg):
    await msg.reply("Chat ID: `{}`".format(msg.chat_id))


@new_cmd(pattern="setgpic|setgp|setdesc|setgdesc|setgname|setgtitle")
async def set_group_info(msg):
    command = msg.text.split(" ")[0][1:].lower()
    if command in ["setgpic", "setgp"]:
        reply = await msg.get_reply_message()
        if not reply:
            await msg.reply("Reply to a photo!")
            return
        if not reply.media:
            await msg.reply("Reply to a photo!")
            return
        if not reply.media.photo:
            await msg.reply("Reply to a photo to set it as group photo!")
            return
        try:
            await msg.client(
                functions.messages.EditChatPhotoRequest(
                    msg.chat_id,
                    reply.media.photo.file_id,
                )
            )
            await msg.reply("Successfully set group photo!")
        except Exception as ex:
            await msg.reply(str(ex) + str(type(ex)))
    elif command in ["setdesc", "setgdesc"]:
        content = await get_text_content(msg)
        if not content:
            await msg.reply("Specify a description!")
            return
        try:
            await msg.client(
                functions.messages.EditChatAboutRequest(msg.chat_id, content)
            )
            await msg.reply("Successfully set group description!")
        except Exception as ex:
            await msg.reply(str(ex) + str(type(ex)))
    elif command in ["setgname", "setgtitle"]:
        content = await get_text_content(msg)
        if not content:
            await msg.reply("Specify a name!")
            return
        try:
            await msg.client(functions.channels.EditTitleRequest(msg.chat_id, content))
            await msg.reply("Successfully set group name!")
        except Exception as ex:
            await msg.reply(str(ex) + str(type(ex)))


@new_cmd(pattern="adminlist")
async def adminlist(msg):
    admins = await msg.client.get_participants(
        msg.chat_id, filters=types.ChannelParticipantsAdmins
    )
    admins = [get_mention(x) for x in admins]
    await msg.reply("Admins in this chat: " + ", ".join(admins))


__help__ = """
<b>Help for Admin module.</b>
 - <code>/adminlist</code>: list of admins in chat
 - <code>/chatid</code>: get the current chat id

 - <code>/setgpic</code>: reply to a photo to set group photo
 - <code>/setgdesc</code>: <text> to set group description
 - <code>/setgtitle</code>: <text> to set group title

 - <code>/ban</code>: bans user from group
 - <code>/sban</code>: silent ban, no message sent to the user
 - <code>/tban</code>: temporary ban for x time
 - <code>/unban</code>: unbans user from group

 - <code>/kick</code>: kicks user from group
 - <code>/skick</code>: silent kick, no message sent to the user

 - <code>/tmute</code>: temporary mute for x time
 - <code>/smute</code>: silent mute, no message sent to the user
 - <code>/mute</code>: mute user in group, works on admins too
 - <code>/unmute</code>: unmute user from group, works on admins too

 - <code>/kickme</code>: kicks user from group (user command)
 - <code>/unbanall</code>: unbans all users from group
 - <code>/cleanup</code>: deletes messages from user in group
 - <code>/cleangroups</code>: deletes messages from all groups
 - <code>/cleanbans</code>: deletes all banned users from groups
 - <code>/<code>cleanbots</code> bans all bots from groups
 - <code>/<code>cleanall</code>: deletes all messages from groups
"""
