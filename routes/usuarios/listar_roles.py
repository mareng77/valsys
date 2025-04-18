from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas.usuario import RolResponse
from typing import List

router = APIRouter()

@router.get("/{id_usuario}/roles", response_model=List[RolResponse])
def listar_roles(id_usuario: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return [{"nombre": rol.nombre} for rol in usuario.roles]