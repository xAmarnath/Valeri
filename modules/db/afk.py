from .db import DB
from time import time

afk = DB.afk

AFK = []


def is_afk(user_id: int):
    return user_id in AFK


def set_afk(user_id: int, name: str, reason: str = "", mode: bool = True):
    if mode:
        afk.update_one({"user_id": user_id}, {
            "$set": {"reason": reason, "time": time(), "name": name}}, upsert=True)
        return AFK.append(user_id) if not is_afk(user_id) else None
    else:
        afk.delete_one({"user_id": user_id})
        return AFK.remove(user_id) if is_afk(user_id) else None


def get_afk(user_id: int):
    return afk.find_one({"user_id": user_id})


def load_afk_on_startup():
    for user_id in afk.find():
        AFK.append(user_id["user_id"])


load_afk_on_startup()
