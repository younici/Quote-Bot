from db.orm.models.admins import Admins
from db.orm.session import AsyncSessionLocal
from sqlalchemy import select

import config.cfg as cfg

async def init_conf():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Admins.tg_id)
        )
        ids = [tg_id for (tg_id,) in result.fetchall()]

        cfg.BASE_ADMIN_IDS = list(set(ids + cfg.BASE_ADMIN_IDS))