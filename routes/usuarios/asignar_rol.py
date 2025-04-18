# routes/usuarios/assign_role.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas.usuario import RolCreate, RolResponse

router = APIRouter()

@router.post("/{id_usuario}/roles", response_model=RolResponse)
def asignar_rol(id_usuario: int, rol: RolCreate, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    rol_existente = db.query(models.Rol).filter(models.Rol.nombre == rol.nombre).first()
    if rol_existente:
        if rol_existente in usuario.roles:
            raise HTTPException(status_code=400, detail="El rol ya está asignado")
        usuario.roles.append(rol_existente)
    else:
        db_rol = models.Rol(nombre=rol.nombre)
        db.add(db_rol)
        db.commit()
        db.refresh(db_rol)
        usuario.roles.append(db_rol)
    db.commit()
    return {"nombre": rol.nombre}