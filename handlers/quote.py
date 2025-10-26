from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy import select, func

from db.orm.models.quotes import Quotes
from db.orm.session import AsyncSessionLocal

from random import randint

router = Router()
@router.message(Command('quote'))
async def give_quote_cmd(msg: Message):
    async with AsyncSessionLocal() as conn:
        result = await conn.execute(select(func.count(Quotes.id)))

        count = result.scalar_one()

        if count > 0:
            quote = await get_quote()
            await msg.answer(quote.content)
        else:
            await msg.answer("админ ещё не занёс фразы")


async def get_quote():
    async with AsyncSessionLocal() as conn:
        result = await conn.execute(select(func.count(Quotes.id)))
        count = result.scalar_one()

        if count == 0:
            return None

        for _ in range(5):
            random_id = randint(1, count)
            quote_result = await conn.execute(select(Quotes).where(Quotes.id == random_id))
            quote = quote_result.scalar_one_or_none()
            if quote:
                return quote

        return None