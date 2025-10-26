from sqlalchemy import Column, Integer, Text, String
from db.orm.base import Base

class Quotes(Base):
    __tablename__ = "quotes"

    id = Column(Integer, autoincrement=True, primary_key=True)
    content = Column(Text, nullable=False)