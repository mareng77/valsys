from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas.cuenta import CuentaResponse
from typing import List

router = APIRouter()

@router.get("/", response_model=List[CuentaResponse])
def listar_cuentas(db: Session = Depends(get_db)):
    cuentas = db.query(models.Cuenta).all()
    return cuentas