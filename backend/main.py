from fastapi import APIRouter, FastAPI
from sqlmodel import SQLModel
from db import engine
from dotenv import load_dotenv
from os import getenv
from router import data_router, auth_router

def create_tables():
    SQLModel.metadata.create_all(engine)

load_dotenv()
app = FastAPI(
        title=getenv("NAME"),
        redoc_url=None
    )

router = APIRouter()
router.include_router(auth_router)
router.include_router(data_router)

app.include_router(router=router)

@app.on_event("startup")
def on_startup():
    create_tables()