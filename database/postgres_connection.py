from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from database.settings import settings


SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "connect_timeout": 5
    }
)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:
        db.close()
