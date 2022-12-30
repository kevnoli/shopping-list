from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from os import getenv
from router import data_router, auth_router

load_dotenv()
app = FastAPI(
    title=getenv("NAME"),
    redoc_url=None
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

router = APIRouter()
router.include_router(auth_router)
router.include_router(data_router)

app.include_router(router=router)
