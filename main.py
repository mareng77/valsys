# main.py
from fastapi import FastAPI
from routes import usuarios_router, cuentas_router, activos_router, crear_transacciones_router, listar_transacciones_router

app = FastAPI()

app.include_router(usuarios_router, prefix="/api/v1", tags=["usuarios"])
app.include_router(cuentas_router, prefix="/api/v1", tags=["cuentas"])
app.include_router(activos_router, prefix="/api/v1", tags=["activos"])
app.include_router(crear_transacciones_router, prefix="/api/v1", tags=["transacciones"])
app.include_router(listar_transacciones_router, prefix="/api/v1", tags=["transacciones"])