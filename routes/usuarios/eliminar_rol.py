from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas.usuario import RolResponse

router = APIRouter()

@router.delete("/{id_usuario}/roles/{rol_nombre}", response_model=RolResponse)
def eliminar_rol(id_usuario: int, rol_nombre: str, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    rol = db.query(models.Rol).filter(models.Rol.nombre == rol_nombre).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    if rol not in usuario.roles:
        raise HTTPException(status_code=400, detail="El rol no está asignado al usuario")
    usuario.roles.remove(rol)
    db.commit()
    return {"nombre": rol.nombre}