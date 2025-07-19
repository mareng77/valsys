from fastapi import APIRouter
from .crear_transacciones import crear_transacciones_router as crear_transacciones_router
from .listar_transacciones import listar_transacciones_router as listar_transacciones_router


listar_transacciones_router = APIRouter(prefix="/listar_transacciones", tags=["transacciones"])
listar_transacciones_router.include_router(listar_transacciones_router)


crear_transacciones_router = APIRouter(prefix="/crear_transacciones", tags=["crear_transacciones"])
crear_transacciones_router.include_router(crear_transacciones_router)

