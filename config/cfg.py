from db.orm.models.admins import Admins
from db.orm.session import AsyncSessionLocal
from sqlalchemy import select

BASE_ADMIN_IDS = [1610414602]
DATABASE_PATH = "./DataBase/data.db"

async def init_conf():
    global BASE_ADMIN_IDS
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Admins.tg_id)
        )
        ids = [tg_id for (tg_id,) in result.fetchall()]

        BASE_ADMIN_IDS = list(set(ids + BASE_ADMIN_IDS))