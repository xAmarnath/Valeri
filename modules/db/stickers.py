from modules.db.db import DB

stickers = DB.stickers


def new_pack(user_id, name, pack_id, animated, video):
    pack = {
        "name": name,
        "pack_id": pack_id,
        "animated": animated,
        "video": video,
        "count": 1,
    }
    stickers.update_one(
        {"user_id": user_id},
        {"$push": {"packs": pack}},
        upsert=True,
    )


def get_packs(user_id):
    s = stickers.find_one({"user_id": user_id})
    if s:
        return s["packs"]
    return []


def get_pack(user_id, animated=False, video=False):
    packs = get_packs(user_id)
    packs.reverse()
    for pack in packs:
        if animated and pack["animated"]:
            return pack
        elif video and pack["video"]:
            return pack
    return pack[-1]
