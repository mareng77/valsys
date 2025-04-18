# routes/activos/create_activo.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas.activo import ActivoCreate

router = APIRouter()

@router.post("/", response_model=ActivoCreate)
def crear_activo(activo: ActivoCreate, db: Session = Depends(get_db)):
    db_activo = models.Activo(
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