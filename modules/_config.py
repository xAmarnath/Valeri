from logging import basicConfig, StreamHandler, INFO
from os import getenv
from dotenv import load_dotenv
from telethon import TelegramClient
import time
from pymongo import MongoClient, errors

basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    level=INFO,
    handlers=[StreamHandler()],
)

StartTime = time.time()

# Load .env file
load_dotenv()

# Environment variables
TOKEN = getenv("TOKEN")
API_KEY = getenv("API_KEY")
API_HASH = getenv("API_HASH")
MONGO_DB = getenv("MONGO_DB")
OWNER_ID = int(getenv("OWNER_ID", "0"))

# clients
bot = TelegramClient(None, api_id=API_KEY, api_hash=API_HASH,
                     device_model="iPhone XS", lang_code="en")
db = MongoClient(MONGO_DB, connect=True)

try:
    db.list_databases()
except errors.ConnectionFailure:
    print("Could not connect to MongoDB")