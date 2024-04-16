# Valeri - Multi Purpose Telegram Bot

## Description

Valeri is a multi purpose telegram bot written in python using telethon. Its initially for personal use but available for public use.

## Features
- [x] Torrent Downloader
- [x] Eval / Exec / Shell
- [x] Sudo Support
- [x] Custom Plugins
- [x] Chatgpt, Dalle & Gemini
- [x] Youtube Song Downloader
- [x] TeraBox Downloader
- [x] Powerfull File Manager
- [x] Custom File Uploader
- [x] Paste, Imdb, Translate
- [x] Weather, Wiki
- [x] Pinterest Search
- [x] Media AFK
- [x] Support for MongoDB or SQLite

## Deploy
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/AmarnathCJD/Valeri)


## Config Vars
- `API_KEY` - Get this from my.telegram.org
- `API_HASH` - Get this from my.telegram.org
- `OWNER_ID` - Your Telegram ID (Not Username) [for owner only commands]
- `MONGO_DB` - Your MongoDB URL (optional)
- `TOKEN` - Your bot token
- `OPENAI_API_KEY` - Your OpenAI API Key (optional)
- `GEMINI_API_KEY` - Your Gemini API Key (optional)
- `SUPPORT_CHAT` - Your Support Chat ID (optional)

## Local Deploy

```bash
git clone https://github.com/amarnathcjd/valeri.git
cd valeri

# Install Requirements
pip3 install -r requirements.txt

# create a .env file and fill the required variables

# Run the bot
python3 -m valeri
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
