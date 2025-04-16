# routes/transacciones/crear.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.transaccion import TransaccionCreate
from services.transacciones import validar_y_crear_transaccion

crear_transacciones_router = APIRouter(prefix="/transacciones", tags=["transacciones"])

@crear_transacciones_router.post("/", response_model=TransaccionCreate)
def crear_transaccion(transaccion: TransaccionCreate, db: Session = Depends(get_db)):
    validar_y_crear_transaccion(db, transaccion)
    return transaccion