# routes/usuarios/create_user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas.usuario import UsuarioCreate, UsuarioResponse

router = APIRouter()

@router.post("/", response_model=UsuarioResponse)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    email_existente = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if email_existente:
        raise HTTPException(status_code=400, detail="El email ya está en uso")
    db_usuario = models.Usuario(
        nombre_completo=usuario.nombre_completo,
        email=usuario.email,
        contraseña_hash=usuario.contraseña_hash,
        telefono=usuario.telefono
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario