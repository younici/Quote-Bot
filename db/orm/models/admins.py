from sqlalchemy import Column, Integer, String
from db.orm.base import Base

class Admins(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer, nullable=False)
    username = Column(String(50), nullable=True)
    name = Column(String(50), nullable=True)