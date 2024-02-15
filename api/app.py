from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.config.postgres import init_postgres_db
from api.controllers import main_router
from api.models import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    init_postgres_db()

    yield


app = FastAPI(
    lifespan=lifespan,
    title="API - UPE Events Management System",
    version="0.1.0",
    description="Sistema de gerenciamento de eventos da UPE - Campus Garanhuns.",
)

app.include_router(main_router)
