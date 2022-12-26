from os import getenv
from sqlmodel import Session, create_engine
from dotenv import load_dotenv
from redis import Redis

load_dotenv()

engine = create_engine(getenv("DB_CONN"), echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def get_redis_client():
    return Redis(host=getenv("REDIS_HOST"), port=6379, db=0)