from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas.cuenta import CuentaResponse
from typing import List

listar_cuentas_router = APIRouter()

@listar_cuentas_router.get("/", response_model=List[CuentaResponse])
def listar_cuentas(db: Session = Depends(get_db)):
    try:
        cuentas = db.query(models.Cuenta).all()
        print(f"Cuentas encontradas: {len(cuentas)}")  # Depuración
        if not cuentas:
            raise HTTPException(status_code=404, detail="No se encontraron cuentas")
        return cuentas
    except Exception as e:
        print(f"Error al listar cuentas: {str(e)}")  # Depuración
        raise HTTPException(status_code=500, detail=f"Error al listar cuentas: {str(e)}")