# main.py
from fastapi import FastAPI
import models
from database import engine, Base
from sqlalchemy.orm import configure_mappers

app = FastAPI(
    title="VALSYS API",
    description="API para la gestión de usuarios, cuentas y activos financieros",
    version="1.0.0"
)

# Configurar mappers y crear tablas antes de importar rutas
configure_mappers()
Base.metadata.create_all(bind=engine)

# Importar rutas después de la configuración de mappers para evitar carga prematura de modelos
from routes import usuarios_router, cuentas_router, activos_router, crear_transacciones_router, listar_transacciones_router

app.include_router(usuarios_router, prefix="/api/v1", tags=["usuarios"])
app.include_router(cuentas_router, prefix="/api/v1", tags=["cuentas"])
app.include_router(activos_router, prefix="/api/v1", tags=["activos"])
app.include_router(crear_transacciones_router, prefix="/api/v1", tags=["transacciones"])
app.include_router(listar_transacciones_router, prefix="/api/v1", tags=["transacciones"])

@app.get("/")
async def root():
    return {"message": "Bienvenido a VALSYS API"}