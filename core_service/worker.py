from fastapi import Depends
from sqlalchemy.orm import Session

from database.model import Data
from database.postgres_connection import get_db, SessionLocal


async def save_data(item: str):

    db = SessionLocal()

    try:
        data = Data(text=item)
        db.add(data)
        db.commit()
    finally:
        db.close()
