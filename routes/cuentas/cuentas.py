# routes/cuentas.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import get_db
import models
from schemas.cuenta import CuentaCreate, CuentaResponse
from schemas.portafolio import PortafolioResponse
from typing import List

cuentas_router = APIRouter(prefix="/cuentas", tags=["cuentas"])

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

@cuentas_router.get("/{id_usuario}/cuentas", response_model=List[CuentaResponse])
def listar_cuentas(id_usuario: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    cuentas = db.query(models.Cuenta).filter(models.Cuenta.id_usuario == id_usuario).all()
    return cuentas

@cuentas_router.get("/{id_cuenta}/portafolios", response_model=List[PortafolioResponse])
def listar_portafolios(id_cuenta: int, db: Session = Depends(get_db)):
    cuenta = db.query(models.Cuenta).filter(models.Cuenta.id_cuenta == id_cuenta).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    portafolios = db.query(models.Portafolio).filter(models.Portafolio.id_cuenta == id_cuenta).all()
    return portafolios