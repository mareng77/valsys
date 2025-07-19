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


# importaciones usuarios
from routes.usuarios.crear_usuario import crear_usuario_router as crear_usuario_router
from routes.usuarios.listar_roles import listar_roles_router as listar_roles_router
from routes.usuarios.eliminar_rol import eliminar_rol_router as eliminar_rol_router
from routes.usuarios.asignar_rol import asignar_rol_router as asignar_rol_router
from routes.usuarios.obtener_contacto import obtener_contacto_router as obtener_contacto_router
# importaicones activos
from routes.activos.crear_activo import crear_activo_router as crear_activo_router
from routes.activos.listar_activo import listar_activo_router as listar_activo_router
# importaciones cuentas
from routes.cuentas.crear_cuenta import crear_cuenta_router as crear_cuenta_router
from routes.cuentas.listar_cuentas import listar_cuentas_router as listar_cuentas_router
from routes.cuentas.listar_portafolios import listar_portafolios_router as listar_portafolios_router
# importaciones transacciones
from routes.transacciones.listar_transacciones import listar_transacciones_router as listar_transacciones_router
from routes.transacciones.crear_transacciones import crear_transacciones_router as crear_transacciones_router



#APIS USUARIOS Y ROLES
app.include_router(crear_usuario_router, prefix="/api/v1", tags=["usuarios"])
app.include_router(listar_roles_router, prefix="/api/v1", tags=["roles"])
app.include_router(eliminar_rol_router, prefix="/api/v1", tags=["roles"])
app.include_router(asignar_rol_router, prefix="/api/v1", tags=["roles"])
app.include_router(obtener_contacto_router, prefix="/api/v1", tags=["usuarios"])

# APIS ACTIVOS
app.include_router(crear_activo_router, prefix="/api/v1", tags=["activos"])
app.include_router(listar_activo_router, prefix="/api/v1", tags=["activos"] )

# APIS CUENTAS
app.include_router(crear_cuenta_router, prefix="/api/v1", tags=["cuentas"])
app.include_router(listar_cuentas_router, prefix="/api/v1", tags=["cuentas"])
app.include_router(listar_portafolios_router, prefix="/api/v1", tags=["cuentas"])

#APIS TRANSACCIONES
app.include_router(crear_transacciones_router, prefix="/api/v1", tags=["transacciones"])
app.include_router(listar_transacciones_router, prefix="/api/v1", tags=["transacciones"])


@app.get("/")
async def root():
    return {"message": "Bienvenido a VALSYS API"}