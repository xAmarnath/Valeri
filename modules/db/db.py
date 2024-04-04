from .._config import db
import sqlite3

SQ_DB_FILE = "bot.db"  # SQLite database file
DB_MODE = 'mongo'  # Change this to 'sqlite' if you want to use SQLite instead of MongoDB

DB = db

if isinstance(db, sqlite3.Connection):
    DB_MODE = 'sql'
else:
    DB = db.bot

def get_db_stats():
    if DB_MODE == 'sql':
        return get_sqlite_stats()
    
    db_ = db.main  # Get the main database
    db_free = db_.command("dbstats")["dataSize"]
    db_total = db_.command("dbstats")["storageSize"]
    return db_free, db_total

def get_sqlite_stats():
    db_ = db.cursor()
    db_.execute("SELECT page_count FROM pragma_page_count;")
    db_free = db_.fetchone()[0]
    db_.execute("SELECT page_size FROM pragma_page_size;")
    page_size = db_.fetchone()[0]
    
    db_total = db_free * page_size
    return db_free, db_total