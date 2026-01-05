from database.postgres_connection import Base
from sqlalchemy import Column, String, Integer


class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)
