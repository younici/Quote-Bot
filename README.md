# Quote-Bot

A simple Telegram bot built with **aiogram** and **SQLite**, designed to store and send random quotes.

## Features
- Add and get quotes from the database  
- Async architecture (aiogram 3)  
- Easy config and setup  
- SQLite with SQLAlchemy / ORM  

## Setup
```bash
git clone https://github.com/younici/Quote-Bot.git
cd Quote-Bot
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt```

Create .env file:
TG_BOT_TOKEN=your_token_here

Run the bot:
python main.py
Project Structure
Quote-Bot/
├─ db/           # database & ORM
├─ handlers/     # command handlers
├─ config/       # config/init
└─ main.py       # entry point
