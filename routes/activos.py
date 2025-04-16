# routes/activos.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Activo
from schemas.activo import ActivoCreate

activos_router = APIRouter(prefix="/activos", tags=["activos"])

@activos_router.post("/", response_model=ActivoCreate)
def crear_activo(activo: ActivoCreate, db: Session = Depends(get_db)):
    db_activo = Activo(
        tipo_activo=activo.tipo_activo,
        nombre_activo=activo.nombre_activo,
        ticker=activo.ticker,
        precio_actual=activo.precio_actual,
        mercado=activo.mercado
    )
    db.add(db_activo)
    db.commit()
    db.refresh(db_activo)
    return activo