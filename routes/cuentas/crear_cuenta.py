# routes/cuentas/create_cuenta.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import get_db
import models
from schemas.cuenta import CuentaCreate, CuentaResponse

router = APIRouter()

@cuentas_router.post("/", response_model=CuentaResponse)
def crear_cuenta(cuenta: CuentaCreate, db: Session = Depends(get_db)):
    try:
        usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == cuenta.id_usuario).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        db_cuenta = models.Cuenta(
            id_usuario=cuenta.id_usuario,
            saldo_disponible=cuenta.saldo_disponible,
            moneda=cuenta.moneda,
            estado=cuenta.estado
        )
        db.add(db_cuenta)
        db.commit()
        db.refresh(db_cuenta)
        return db_cuenta
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")