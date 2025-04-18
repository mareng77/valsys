# routes/usuarios.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas.usuario import UsuarioCreate, UsuarioResponse, ContactInfo, RolCreate, RolResponse
from typing import List

usuarios_router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@usuarios_router.post("/", response_model=UsuarioResponse)
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

@usuarios_router.get("/{id_usuario}/contacto", response_model=ContactInfo)
def obtener_contacto(id_usuario: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {
        "nombre_completo": usuario.nombre_completo,
        "email": usuario.email,
        "telefono": usuario.telefono
    }

@usuarios_router.post("/{id_usuario}/roles", response_model=RolResponse)
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

@usuarios_router.get("/{id_usuario}/roles", response_model=List[RolResponse])
def listar_roles(id_usuario: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return [{"nombre": rol.nombre} for rol in usuario.roles]

@usuarios_router.delete("/{id_usuario}/roles/{rol_nombre}", response_model=RolResponse)
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