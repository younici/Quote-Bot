from aiogram import Dispatcher, Bot
import asyncio
from db.orm.utils import init_db

from dotenv import load_dotenv
import os

from handlers import start, admin, quote

load_dotenv()

TOKEN = os.getenv('TG_BOT_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    await init_db()
    dp.include_routers(start.router, admin.router, quote.router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())