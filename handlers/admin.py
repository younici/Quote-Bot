from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from sqlalchemy import select

import config.cfg as cfg
from config.init import init_conf
from db.orm.models.admins import Admins
from db.orm.session import AsyncSessionLocal
from db.orm.models.quotes import Quotes

from decorators.admin_only import admin_only

NOT_ALLOWED_ANSWER = "У вас нет прав для использования этой команды."
ADD_QUOTE_INVALID_ARGUMENT = "Добавьте текст для фразы \n/<command> <text>"

router = Router()

@admin_only
@router.message(Command("add_quote"))
async def admin_add_quote_cmd(msg: Message, cmd: CommandObject | None = None):
    quote_text = await get_text(msg, cmd)
    if quote_text is None:
        await msg.answer(ADD_QUOTE_INVALID_ARGUMENT)
        return

    async with AsyncSessionLocal() as conn:
        result = await conn.execute(select(Quotes).where(Quotes.content == quote_text))

        if result.scalar_one_or_none() is not None:
            await msg.answer("Фраза уже существует в базе данных")
            return

        new_quote = Quotes(content=quote_text)
        conn.add(new_quote)
        await conn.commit()
    await msg.answer(f'Фраза "{quote_text}" успешно добавлена')

@admin_only
@router.message(Command("get_quote_id"))
async def get_quote_id_cmd(msg: Message, cmd: CommandObject | None = None):
    quote_text = await get_text(msg, cmd)
    if quote_text is None:
        await msg.answer(ADD_QUOTE_INVALID_ARGUMENT)
        return
    async with AsyncSessionLocal() as conn:
        result = await conn.execute(select(Quotes).where(Quotes.content == quote_text))
        quote = result.scalar_one_or_none()
        if quote is None:
            await msg.answer("Фраза не найдена")
        await msg.answer(f"Айди фразы {quote.id}")

@admin_only
@router.message(Command("dell_quote"))
async def dell_quote_cmd(msg: Message, cmd: CommandObject | None = None):
    id = await get_int(msg, cmd)
    if id is None:
        await msg.answer("Введите корректный id")
        return
    async with AsyncSessionLocal() as conn:
        result = await conn.execute(select(Quotes).where(Quotes.id == id))
        quote = result.scalar_one_or_none()
        if quote is None:
            await msg.answer("Данного айди нету в базе данных")
            return
        await conn.delete(quote)
        await conn.commit()
        await msg.answer("Фраза успешно удалена")

@admin_only
@router.message(Command("add_admin"))
async def add_admin_cmd(msg: Message, cmd: CommandObject | None = None):
    id = await get_int(msg, cmd)
    if id is None:
        await msg.answer("Введите айди человека которого хотите поставить на должность администратора")
        return
    admin = await try_get_user(id, msg)
    if admin is None:
        await msg.answer("Этот человек не взаимодействовал с ботом.")
        return
    async with AsyncSessionLocal() as conn:
        result = await conn.execute(select(Admins).where(Admins.tg_id == id))
        if result.scalar_one_or_none() is not None:
            await msg.answer(f"Админ с телеграмм айди {id} уже записан в базе данных")
            return
        new_admin = Admins(tg_id=id, username=admin.username, name=admin.first_name)
        conn.add(new_admin)
        await conn.commit()
        await msg.answer("Админ Успешно добавлен")
        await init_conf()

@admin_only
@router.message(Command("dell_admin"))
async def dell_admin_cmd(msg: Message, cmd: CommandObject | None = None):
    id = await get_int(msg, cmd)
    if id is None:
        await msg.answer("Введите телеграмм айди человека")
        return
    async with AsyncSessionLocal() as conn:
        result = await conn.execute(select(Admins).where(Admins.tg_id == id))
        admin = result.scalar_one_or_none()
        if admin is None:
            await msg.answer(f"Админа с телеграмм айди {id} нету в базе данных")
        await conn.delete(admin)
        await conn.commit()
        cfg.BASE_ADMIN_IDS.remove(id)
        await msg.answer("Админ успешно удалён с базы данных")

async def get_int(msg: Message, cmd: CommandObject | None = None):
    text = await get_text(msg, cmd)
    try:
        return int(text)
    except:
        return None

async def get_text(msg: Message, cmd: CommandObject | None = None):
    try:
        quote_text = ""
        if cmd is None:
            text = msg.text.split(maxsplit=1)
            if 2 < len(text):
                await msg.answer(ADD_QUOTE_INVALID_ARGUMENT)
            else:
                quote_text = text[1].strip()
        else:
            quote_text = cmd.args.strip()
        return quote_text
    except IndexError:
        return None

async def try_get_user(id: int, msg: Message):
    bot = msg.bot
    try:
        return await bot.get_chat(id)
    except Exception:
        return None