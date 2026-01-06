import os
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import socket

from database.model import Data
from database.postgres_connection import get_db
from database.redis_connection import redis_client

app = FastAPI()


@app.get("/health")
async def health_point():
    return {"status": "ok", "instance": socket.gethostname()}


@app.post("/data/{item}")
async def create_data(item: str, db: Session = Depends(get_db)):
    data = Data(text=item)
    db.add(data)
    db.commit()
    db.refresh(data)
    return {"id": data.id, "Message": data.text}


@app.get("/data/{item}")
async def read_data(item: int, db: Session = Depends(get_db)):
    cache_key = f"Data:{item}"

    # try cache
    cached = redis_client.get(cache_key)

    if cached:
        return {"source": "cache", "data": cached}

    # cache miss -> db
    result = db.query(Data).filter(Data.id == item).first()
    if not result:
        return {"Message": "Data not found"}
    # store in cache
    redis_client.setex(cache_key, 60, result.text)

    return {"source": "db", "data": result.text}
