from .db import DB

stats = DB.stats


def add_chat(chat_id):
    stats.update_one({"_id": "chats"}, {"$inc": {"count": 1}}, upsert=True)
    stats.update_one({"_id": "chats"}, {"$addToSet": {
                     "chat_ids": chat_id}}, upsert=True)
    return True


def add_user(user_id):
    stats.update_one({"_id": "users"}, {"$inc": {"count": 1}}, upsert=True)
    stats.update_one({"_id": "users"}, {"$addToSet": {
                     "user_ids": user_id}}, upsert=True)
    return True


def get_chat_count():
    chats = stats.find_one({"_id": "chats"})
    if chats is None:
        return 0
    return chats["count"]


def get_user_count():
    users = stats.find_one({"_id": "users"})
    if users is None:
        return 0
    return users["count"]


def get_chat_ids():
    chats = stats.find_one({"_id": "chats"})
    if chats is None:
        return []
    return chats["chat_ids"]


def get_user_ids():
    users = stats.find_one({"_id": "users"})
    if users is None:
        return []
    return users["user_ids"]

def already_added_user(user_id):
    users = stats.find_one({"_id": "users"})
    if users is None:
        return False
    return user_id in users["user_ids"]