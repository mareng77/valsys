from fastapi import APIRouter
from .crear_activo import crear_activo_router as crear_activo_router
from .listar_activo import listar_activo_router as listar_activo_router


crear_activo_router = APIRouter(prefix="/activos", tags=["activos"])
crear_activo_router.include_router(crear_activo_router)

listar_activo_router = APIRouter(prefix="/listar_activo", tags=["listar_activo"])
listar_activo_router.include_router(listar_activo_router)