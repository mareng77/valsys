from fastapi import APIRouter
from .crear_usuario import crear_usuario_router as crear_usuario_router
from .listar_roles import listar_roles_router as listar_roles_router
from .eliminar_rol import eliminar_rol_router as eliminar_rol_router
from .asignar_rol import asignar_rol_router as asignar_rol_router
from .obtener_contacto import obtener_contacto_router as obtener_contacto_router


crear_usuario_router = APIRouter(prefix="/crear_usuario", tags=["crear_usuario"])
crear_usuario_router.include_router(crear_usuario_router)

listar_roles = APIRouter(prefix="/listar_roles", tags=["listar_roles"])
listar_roles.include_router(listar_roles_router)

eliminar_rol = APIRouter(prefix="/eliminar_rol", tags=["eliminar_rol"])
eliminar_rol.include_router(eliminar_rol_router)

asignar_rol_router = APIRouter(prefix="/asignar_rol", tags=["asignar_rol"])
asignar_rol_router.include_router(asignar_rol_router)

obtener_contacto_router = APIRouter(prefix="/obtener_contacto", tags=["obtener_contacto"])
obtener_contacto_router.include_router(obtener_contacto_router)

