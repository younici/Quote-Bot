from functools import wraps

from aiogram.types import Message

from config.cfg import BASE_ADMIN_IDS

def admin_only(func):
    @wraps(func)
    async def wrapper(msg: Message, *args, **kwargs):
        if  msg.from_user.id in BASE_ADMIN_IDS:
            result = await func(msg, *args, **kwargs)
            return result
        else:
            await msg.answer("У вас нету доступа для выполнения этой команды.")
            return
    return wrapper