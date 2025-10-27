from aiogram import Dispatcher, Bot
import asyncio
from db.orm.utils import init_db

from dotenv import load_dotenv
import os

from config.init import init_conf
import config.cfg as cfg

from handlers import start, admin, quote

load_dotenv()

TOKEN = os.getenv('TG_BOT_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    await init_db()
    await init_conf()
    dp.include_routers(start.router, admin.router, quote.router)
    await dp.start_polling(bot)

async def log():
    while True:
        print(cfg.BASE_ADMIN_IDS)
        await asyncio.sleep(1)

async def start_tasks():
    log_task = asyncio.create_task(log())
    main_task = asyncio.create_task(main())
    await asyncio.gather(main_task, log_task)

if __name__ == '__main__':
    asyncio.run(start_tasks())
