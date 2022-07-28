from datetime import datetime

from .db import DB

warns = DB.warns
warn_settings = DB.warn_settings

CHAT_WARN_SETTINGS = {}
DEFAULT_WARN_SETTINGS = {
    "max_warnings": 3,
    "warn_mode": "kick",
    "warn_time": 1,
    "action_time": 0,
}


def warn_user(user_id, chat_id, reason, warn_by):
    """
    Warns a user in a chat.
    """
    warns.update_one(
        {"user_id": user_id, "chat_id": chat_id},
        {
            "$addToSet": {
                "warnings": {
                    "reason": reason,
                    "warned_by": warn_by,
                    "date": datetime.now(),
                }
            }
        },
        {"$inc": {"warn_count": 1}},
        upsert=True,
    )


def remove_last_warn(user_id, chat_id):
    """
    Removes the last warning from a user in a chat.
    """
    if get_warn_count(user_id, chat_id) == 0:
        return False
    warns.update_one(
        {"user_id": user_id, "chat_id": chat_id}, {"$pop": {"warnings": -1}}
    )
    return True


def remove_all_warns(user_id, chat_id):
    """
    Removes all warnings from a user in a chat.
    """
    if get_warn_count(user_id, chat_id) == 0:
        return False
    warns.delete_one({"user_id": user_id, "chat_id": chat_id})
    return True


def reset_chat_warnings(chat_id):
    """
    Resets the warning settings for a chat.
    """
    warns.delete_many({"chat_id": chat_id})


def get_warn_count(user_id, chat_id):
    """
    Returns the number of warnings a user has in a chat.
    """
    warn = warns.find_one({"user_id": user_id, "chat_id": chat_id})
    if warn is None:
        return 0
    return warn["warn_count"]


def get_warnings(user_id, chat_id):
    """
    Returns a list of warnings a user has in a chat.
    """
    warn = warns.find_one({"user_id": user_id, "chat_id": chat_id})
    if warn is None:
        return []
    return warn["warnings"]


def get_warn_setting(chat_id):
    """
    Returns the warning settings for a chat.
    """
    warn_setting = warn_settings.find_one({"chat_id": chat_id})
    if warn_setting is None:
        return DEFAULT_WARN_SETTINGS
    for key in ["max_warnings", "warn_mode", "warn_time", "action_time"]:
        if key not in warn_setting or warn_setting[key] is None:
            warn_setting[key] = DEFAULT_WARN_SETTINGS[key]
    return warn_setting


def set_warn_setting(chat_id, max_warnings, warn_mode, warn_time, action_time):
    """
    Sets the warning settings for a chat.
    """
    warn_settings.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "max_warnings": max_warnings,
                "warn_mode": warn_mode,
                "warn_time": warn_time,
                "action_time": action_time,
            }
        },
        upsert=True,
    )
    CHAT_WARN_SETTINGS[chat_id] = {
        "max_warnings": max_warnings,
        "warn_mode": warn_mode,
        "warn_time": warn_time,
        "action_time": action_time,
    }
    return True


def reset_warn_settings(chat_id):
    """
    Resets the warning settings for a chat.
    """
    warn_settings.delete_one({"chat_id": chat_id})
    if chat_id in CHAT_WARN_SETTINGS:
        del CHAT_WARN_SETTINGS[chat_id]
    return True


def get_chat_warn_settings(chat_id):
    """
    Returns the warning settings for a chat.
    """
    if chat_id in CHAT_WARN_SETTINGS:
        return CHAT_WARN_SETTINGS[chat_id]
    warn_setting = get_warn_setting(chat_id)
    CHAT_WARN_SETTINGS[chat_id] = warn_setting
    return warn_setting


def get_all_warn_settings():
    """
    Returns all warning settings.
    """
    settings = warn_settings.find()
    if settings is None:
        return []
    return list(settings)


def cache_warn_settings():
    """
    Caches all warning settings.
    """
    settings = get_all_warn_settings()
    for setting in settings:
        CHAT_WARN_SETTINGS[setting["chat_id"]] = setting


cache_warn_settings()
