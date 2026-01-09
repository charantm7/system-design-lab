from fastapi import Depends
from sqlalchemy.orm import Session

from database.model import Data
from database.postgres_connection import get_db


async def save_data(item: str, db: Session = Depends(get_db)):

    try:
        data = Data(item=item)
        db.add(data)
        db.commit
    finally:
        db.close()
