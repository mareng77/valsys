from fastapi import APIRouter
from .create_cuenta import router as create_cuenta_router

cuentas_router = APIRouter(prefix="/cuentas", tags=["cuentas"])

cuentas_router.include_router(create_cuenta_router)