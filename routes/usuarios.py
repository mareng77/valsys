# routes/usuarios.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.usuario import Usuario
from models.rol import Rol
from schemas.usuario import UsuarioCreate, UsuarioResponse, ContactInfo, RolCreate, RolResponse

usuarios_router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@usuarios_router.post("/", response_model=UsuarioCreate)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = Usuario(
        nombre_completo=usuario.nombre_completo,
        email=usuario.email,
        contraseña_hash=usuario.contraseña_hash,
        telefono=usuario.telefono
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return usuario

@usuarios_router.get("/{id_usuario}", response_model=UsuarioResponse)
def obtener_usuario(id_usuario: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@usuarios_router.put("/update-contact/{id_usuario}")
def update_contact(id_usuario: int, contact: ContactInfo, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    email_existente = db.query(Usuario).filter(Usuario.email == contact.email, Usuario.id_usuario != id_usuario).first()
    if email_existente:
        raise HTTPException(status_code=400, detail="El email ya está en uso por otro usuario")

    usuario.nombre_completo = contact.nombre_completo
    usuario.email = contact.email
    usuario.telefono = contact.telefono

    db.commit()
    db.refresh(usuario)

    response = {
        "message": "Información actualizada con éxito",
        "data": {
            "nombre_completo": usuario.nombre_completo,
            "email": usuario.email,
            "telefono": usuario.telefono
        }
    }
    print("Respuesta que se enviará:", response)
    return response

@usuarios_router.post("/roles", response_model=RolCreate)
def crear_rol(rol: RolCreate, db: Session = Depends(get_db)):
    db_rol = Rol(
        nombre_rol=rol.nombre_rol,
        descripcion=rol.descripcion
    )
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return rol

@usuarios_router.post("/{id_usuario}/roles/{id_rol}")
def asignar_rol(id_usuario: int, id_rol: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    rol = db.query(Rol).filter(Rol.id_rol == id_rol).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    if rol in usuario.roles:
        raise HTTPException(status_code=400, detail="El rol ya está asignado al usuario")

    usuario.roles.append(rol)
    db.commit()

    return {"message": f"Rol {rol.nombre_rol} asignado al usuario {usuario.nombre_completo}"}

@usuarios_router.get("/{id_usuario}/roles", response_model=list[RolResponse])
def get_usuario_roles(id_usuario: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario.roles