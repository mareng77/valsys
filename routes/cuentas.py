# routes/cuentas.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from database import get_db
from models.usuario import Usuario
from models.cuenta import Cuenta
from schemas.cuenta import CuentaCreate, CuentaResponse

cuentas_router = APIRouter(prefix="/cuentas", tags=["cuentas"])

@cuentas_router.post("/", response_model=CuentaResponse)
def crear_cuenta(cuenta: CuentaCreate, db: Session = Depends(get_db)):
    try:
        # Validación adicional
        if cuenta.saldo_disponible < 0:
            raise HTTPException(status_code=400, detail="El saldo disponible no puede ser negativo")

        usuario = db.query(Usuario).filter(Usuario.id_usuario == cuenta.id_usuario).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        db_cuenta = Cuenta(
            id_usuario=cuenta.id_usuario,
            saldo_disponible=cuenta.saldo_disponible,
            moneda=cuenta.moneda,
            estado=cuenta.estado
        )
        db.add(db_cuenta)
        db.commit()
        db.refresh(db_cuenta)

        return db_cuenta
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error de integridad en la base de datos: {str(e)}")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

#@cuentas_router.get("/", response_model=list[CuentaResponse])
#async def get_cuentas(db: Session = Depends(get_db)):
#    try:
#        return db.query(Cuenta).all()
#    except SQLAlchemyError as e:
#        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {str(e)}")

@cuentas_router.get("/{id_cuenta}", response_model=CuentaResponse)
async def get_cuenta(id_cuenta: int, db: Session = Depends(get_db)):
    try:
        cuenta = db.query(Cuenta).filter(Cuenta.id_cuenta == id_cuenta).first()
        if not cuenta:
            raise HTTPException(status_code=404, detail="Cuenta no encontrada")
        return cuenta
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {str(e)}")