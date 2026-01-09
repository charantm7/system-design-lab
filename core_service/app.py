import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import socket

from database.model import Data
from database.postgres_connection import SessionLocal, get_db
from database.redis_connection import get_cached, set_cache, queue
from .worker import save_data

app = FastAPI()


@app.get("/health")
async def health_point():
    return {"status": "ok", "instance": socket.gethostname()}


@app.post("/data/{item}")
async def create_data(item: str):

    job = queue.enqueue(save_data, item)

    return {"status": "Accepted", "Job ID": job.id}


@app.get("/data/{item}")
async def read_data(item: int, db: Session = Depends(get_db)):
    cache_key = f"Data:{item}"

    # try cache not db
    cached = await get_cached(cache_key)

    if cached:
        return {"source": "cache", "data": cached}

    # cache miss -> db
    try:

        result = db.query(Data).filter(Data.id == item).first()
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Service temporarily unavailable"
        )
    if not result:
        return {"Message": "Data not found"}
    # store in cache
    await set_cache(key=cache_key, value=result.text)

    return {"source": "db", "data": result.text}
