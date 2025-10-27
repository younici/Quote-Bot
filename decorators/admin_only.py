from functools import wraps

from aiogram.types import Message

import config.cfg as cfg

def admin_only(func):
    @wraps(func)
    async def wrapper(msg: Message, *args, **kwargs):
        if  msg.from_user.id in cfg.BASE_ADMIN_IDS:
            result = await func(msg, *args, **kwargs)
            return result
        else:
            await msg.answer("У вас нету доступа для выполнения этой команды.")
            return
    return wrapper