from fastapi import FastAPI
import models
from database import engine, Base
from sqlalchemy.orm import configure_mappers

app = FastAPI(
    title="VALSYS API",
    description="API para la gestión de usuarios, cuentas y activos financieros",
    version="1.0.0"
)

configure_mappers()
Base.metadata.create_all(bind=engine)

from routes.usuarios import usuarios_router
from routes.activos import activos_router
from routes.cuentas import cuentas_router
from routes.transacciones import crear_transacciones_router, listar_transacciones_router

app.include_router(usuarios_router, prefix="/api/v1", tags=["usuarios"])
app.include_router(activos_router, prefix="/api/v1", tags=["activos"])
app.include_router(cuentas_router, prefix="/api/v1", tags=["cuentas"])
app.include_router(crear_transacciones_router, prefix="/api/v1", tags=["transacciones"])
app.include_router(listar_transacciones_router, prefix="/api/v1", tags=["transacciones"])

@app.get("/")
async def root():
    return {"message": "Bienvenido a VALSYS API"}