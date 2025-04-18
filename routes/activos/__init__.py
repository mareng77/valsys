from fastapi import APIRouter
from .create_activo import router as create_activo_router

activos_router = APIRouter(prefix="/activos", tags=["activos"])

activos_router.include_router(create_activo_router)
