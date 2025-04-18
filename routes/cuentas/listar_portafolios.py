from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas.portafolio import PortafolioResponse
from typing import List

router = APIRouter()

@router.get("/{id_cuenta}/portafolios", response_model=List[PortafolioResponse])
def listar_portafolios(id_cuenta: int, db: Session = Depends(get_db)):
    cuenta = db.query(models.Cuenta).filter(models.Cuenta.id_cuenta == id_cuenta).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    portafolios = db.query(models.Portafolio).filter(models.Portafolio.id_cuenta == id_cuenta).all()
    return portafolios