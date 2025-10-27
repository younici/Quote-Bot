from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

import config.cfg as cfg

router = Router()

HELP_TEXT = """
/quote - Получить случайную фразу
/start - Приветствие
"""
ADMIN_HELP_TEXT = """
/add_quote <text> - Добавить фразу
/dell_quote <id> - Удалить фразу
/get_quote_id <text from quote> - Получить айди фразы по её тексту
/add_admin <telegram_id> - Добавить нового администратора (сработает только если человек начал чат с ботом)
/dell_admin <telegram_id> - Удалить админа
"""

@router.message(Command('start'))
async def start_cmd(msg: Message):
    await msg.answer('Здравствуйте, бот предназначен для выдачи случайных фраз, для получения фразы введите команду /quote')

@router.message(Command('help'))
async def help_cmd(msg: Message):
    await msg.answer(HELP_TEXT)
    if msg.from_user.id in cfg.BASE_ADMIN_IDS:
        await msg.answer(ADMIN_HELP_TEXT)