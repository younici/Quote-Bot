import os.path

from db.orm.base import Base
from db.orm.session import engine

async def init_db():
    if not os.path.exists("./DataBase"):
        os.makedirs("./DataBase")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)