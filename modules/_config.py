import logging
import time
from logging import INFO, basicConfig, getLogger, handlers
from os import getenv

from dotenv import load_dotenv
from pymongo import MongoClient, errors
from telethon import TelegramClient

basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    level=INFO,
)

handler = handlers.RotatingFileHandler(
    "logs.txt", maxBytes=10 * 1024 * 1024, backupCount=10
)
handler.setLevel(INFO)
handler.setFormatter(
    logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )
)
getLogger("").addHandler(handler)


StartTime = time.time()
help_dict = {}

# Load .env file
load_dotenv()

log = getLogger("valeri")
# Environment variables
TOKEN = getenv("TOKEN")
API_KEY = getenv("API_KEY")
API_HASH = getenv("API_HASH")
MONGO_DB = getenv("MONGO_DB")
OWNER_ID = int(getenv("OWNER_ID", "0"))
TMDB_KEY = getenv("TMDB_KEY")  # required for !imdb

# clients
bot = TelegramClient(
    None, api_id=API_KEY, api_hash=API_HASH, device_model="iPhone XS", lang_code="en"
)
db = MongoClient(MONGO_DB, connect=True)

try:
    db.list_databases()
except errors.ConnectionFailure:
    log.info("MongoDB connection failed")
