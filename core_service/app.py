import os
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import socket

from database.model import Data
from database.postgres_connection import get_db

app = FastAPI()


@app.get("/health")
async def health_point():
    return {"status": "ok", "instance": socket.gethostname()}


@app.post("/data")
async def create_data(item: str, db: Session = Depends(get_db)):
    data = Data(text=item)
    db.add(data)
    db.commit()
    db.refresh(data)
    return {"id": data.id, "Message": data.text}


@app.get("/data")
async def read_data(db: Session = Depends(get_db)):
    return db.query(Data).all()
