# schemas/usuario.py
from pydantic import BaseModel
from typing import Optional

class ContactInfo(BaseModel):
    nombre_completo: str
    email: str
    telefono: Optional[str] = None

class UsuarioCreate(BaseModel):
    nombre_completo: str
    email: str
    contraseña_hash: str
    telefono: Optional[str] = None

class UsuarioResponse(BaseModel):
    id_usuario: int
    nombre_completo: str
    email: str
    telefono: Optional[str] = None

    class Config:
        from_attributes = True

class RolCreate(BaseModel):
    nombre_rol: str
    descripcion: Optional[str] = None

class RolResponse(BaseModel):
    id_rol: int
    nombre_rol: str
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True