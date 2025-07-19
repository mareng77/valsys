from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas.activo import ActivoResponse
from typing import List

listar_activo_router = APIRouter()

@listar_activo_router.get("/activos", response_model=List[ActivoResponse])
def listar_activos(db: Session = Depends(get_db)):
    activos = db.query(models.Activo).all()
    return activos