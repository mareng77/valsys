# routes/usuarios/get_contact.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas.usuario import ContactInfo

router = APIRouter()

@router.get("/{id_usuario}/contacto", response_model=ContactInfo)
def obtener_contacto(id_usuario: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {
        "nombre_completo": usuario.nombre_completo,
        "email": usuario.email,
        "telefono": usuario.telefono
    }