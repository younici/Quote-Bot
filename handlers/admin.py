from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from sqlalchemy import select
from db.orm.session import AsyncSessionLocal
from db.orm.models.quotes import Quotes

from config.cfg import BASE_ADMIN_IDS

NOT_ALLOWED_ANSWER = "У вас нет прав для использования этой команды."
ADD_QUOTE_INVALID_ARGUMENT = "Добавьте текст для фразы \n/<command> <text>"

router = Router()

@router.message(Command("add_quote"))
async def admin_add_quote_cmd(msg: Message, cmd: CommandObject | None = None):
    if msg.from_user.id in BASE_ADMIN_IDS:
        quote_text = await get_quote_text(msg, cmd)
        if quote_text is None:
            await msg.answer(ADD_QUOTE_INVALID_ARGUMENT)

        async with AsyncSessionLocal() as conn:
            new_quote = Quotes(content=quote_text)
            conn.add(new_quote)
            await conn.commit()
        await msg.answer(f'Фраза "{quote_text}" успешно добавлена')
    else:
        await msg.answer(NOT_ALLOWED_ANSWER)

@router.message(Command("get_quote_id"))
async def get_quote_id_cmd(msg: Message, cmd: CommandObject | None = None):
    if msg.from_user.id in BASE_ADMIN_IDS:
        quote_text = await get_quote_text(msg, cmd)
        if quote_text is None:
            await msg.answer(ADD_QUOTE_INVALID_ARGUMENT)
        async with AsyncSessionLocal() as conn:
            result = await conn.execute(select(Quotes).where(Quotes.content == quote_text))
            quote = result.scalar_one_or_none()
            if quote is None:
                await msg.answer("Фраза не найдена")
            await msg.answer(f"Айди фразы {quote.id}")
    else:
        await msg.answer(NOT_ALLOWED_ANSWER)


async def get_quote_text(msg: Message, cmd: CommandObject | None = None):
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