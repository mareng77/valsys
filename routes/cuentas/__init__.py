from fastapi import APIRouter
from .crear_cuenta import crear_cuenta_router as crear_cuenta_router
from .listar_cuentas import listar_cuentas_router as listar_cuentas_router
from .listar_portafolios import listar_portafolios_router as listar_portafolios_router



crear_cuenta_router = APIRouter(prefix="/cuentas", tags=["cuentas"])
crear_cuenta_router.include_router(crear_cuenta_router)

listar_cuentas_router = APIRouter(prefix="/listar_cuentas", tags=["listar_cuentas"])
listar_cuentas_router.include_router(listar_cuentas_router)

listar_portafolios_router = APIRouter(prefix="/listar_portafolios", tags=["listar_portafolios"])
listar_portafolios_router.include_router(listar_portafolios_router)


