from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas.usuario import UsuarioCreate, UsuarioResponse, ContactInfo, RolCreate, RolResponse

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
        usuario.roles.append(rol_existente)
    else:
        db_rol = models.Rol(nombre=rol.nombre)
        db.add(db_rol)
        db.commit()
        db.refresh(db_rol)
        usuario.roles.append(db_rol)
    db.commit()
    return {"nombre": rol.nombre}