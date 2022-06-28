from modules.db.db import DB

ADMINS = []


def is_auth(user_id):
    """
    Check if a user is authorized.
    """
    return user_id in ADMINS


def add_auth(user_id):
    """
    Add a user to the list of authorized users.
    """
    if user_id not in ADMINS:
        ADMINS.append(user_id)
        DB.main.update_one({"_id": "auth"}, {"$push": {"admins": user_id}})
        return True
    return False


def remove_auth(user_id):
    """
    Remove a user from the list of authorized users.
    """
    if user_id in ADMINS:
        ADMINS.remove(user_id)
        DB.main.update_one({"_id": "auth"}, {"$pull": {"admins": user_id}})
        return True
    return False


def get_auth():
    """
    Get the list of authorized users.
    """
    return ADMINS


def __init_auth():
    """
    Initialize the list of authorized users.
    """
    global ADMINS
    admins = DB.main.find_one({"_id": "auth"})
    if admins:
        ADMINS.extend(admins["admins"])


__init_auth()

