from fastapi import FastAPI
from api.controllers import main_router

app = FastAPI(
    title="API - UPE Events Management System",
    version="0.1.0",
    description="Sistema de gerenciamento de eventos da UPE - Campus Garanhuns.",
)

app.include_router(main_router)
