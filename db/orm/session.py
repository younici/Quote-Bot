import sqlalchemy.ext.asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from config.cfg import DATABASE_PATH

db_url = f"sqlite+aiosqlite:///{DATABASE_PATH}"

engine = create_async_engine(db_url)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession) # type: sqlalchemy.ext.asyncio