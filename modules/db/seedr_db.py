from .db import DB

seedr = DB.seedr  # collection seedr


def get_seedr(user_id):
    """
    Get the seedr object for a user.
    """
    user = seedr.find_one({"user_id": user_id})
    if user:
        return user["token"]
    return None


def update_seedr(user_id, token):
    """
    Update the seedr object for a user.
    """
    seedr.update_one({"user_id": user_id}, {"$set": {"token": token}}, upsert=True)
