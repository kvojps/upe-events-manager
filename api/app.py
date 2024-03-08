from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.config.postgres import init_postgres_db
from api.controllers import main_router
from api.models import init_config_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_config_db()
    init_postgres_db()

    yield


app = FastAPI(
    lifespan=lifespan,
    title="API - UPE Events Management System",
    version="0.1.0",
    description="Sistema de gerenciamento de eventos da UPE - Campus Garanhuns.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)
