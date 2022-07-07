from .db import DB

welcome = DB.welcome

welcome_blacklist = []


def set_welcome(chat_id, file, caption):
    welcome.update_one(
        {"chat_id": chat_id}, {"$set": {"file": file, "caption": caption}}, upsert=True
    )


def set_welcome_mode(chat_id, mode):
    welcome.update_one({"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True)


def set_welcome_clean(chat_id, clean):
    welcome.update_one({"chat_id": chat_id}, {"$set": {"clean": clean}}, upsert=True)


def set_welcome_captcha(chat_id, captcha):
    welcome.update_one(
        {"chat_id": chat_id}, {"$set": {"captcha": captcha}}, upsert=True
    )


def get_welcome(chat_id):
    return welcome.find_one({"chat_id": chat_id}) or {
        "chat_id": chat_id,
        "file": [],
        "captcha": False,
        "mode": True,
        "caption": "Hi {first_name}, welcome to {title}",
        "clean": False,
    }


def get_welcome_mode(chat_id):
    return get_welcome(chat_id).get("mode", True)


def get_welcome_captcha(chat_id):
    return get_welcome(chat_id).get("captcha", False)


def get_welcome_clean(chat_id):
    return get_welcome(chat_id).get("clean", False)


def get_welcome_raw(chat_id):
    return get_welcome(chat_id).get("caption", "Hi {first_name}, welcome to {title}")


# soon
