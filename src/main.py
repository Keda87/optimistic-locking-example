import os
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise

from app.routers import users, vouchers
from config.database import init_database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost',
        'http://localhost:8000',
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix='/api')
app.include_router(vouchers.router, prefix='/api')


@app.on_event("startup")
async def startup():
    await init_database()


@app.on_event("shutdown")
async def shutdown():
    await Tortoise.close_connections()


@app.get("/")
async def index():
    return {
        'pid': os.getpid(),
        'time': time.time(),
        'status': 'OK',
    }
