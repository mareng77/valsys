# routes/transacciones/listar.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
from services.transacciones import obtener_transacciones_por_cuenta
from schemas.transaccion import TransaccionCreate
from typing import List

listar_transacciones_router = APIRouter(prefix="/transacciones", tags=["transacciones"])

@listar_transacciones_router.get("/{id_cuenta}", response_model=List[TransaccionCreate])
def listar_transacciones(id_cuenta: int, db: Session = Depends(get_db)):
    transacciones = obtener_transacciones_por_cuenta(db, id_cuenta)
    return transacciones