from .._config import db

DB = db.bot # Get the bot database

def get_db_stats():
    db_ = db.main  # Get the main database
    db_free = db_.command("dbstats")["dataSize"]
    db_total = db_.command("dbstats")["storageSize"]
    return db_free, db_total
