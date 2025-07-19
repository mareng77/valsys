# routes/__init__.py

#usuarios
from .usuarios.crear_usuario import crear_usuario_router
from .usuarios.listar_roles import listar_roles_router
from .usuarios.eliminar_rol import eliminar_rol_router
from .usuarios.asignar_rol import asignar_rol_router
from .usuarios.obtener_contacto import obtener_contacto_router

#cuentas
from .cuentas.crear_cuenta import crear_cuenta_router
from .cuentas.listar_cuentas import listar_cuentas_router
from .cuentas.listar_portafolios import listar_portafolios


#activos
from .activos.crear_activo import crear_activo_router
from .activos.listar_activo import listar_activo_router

#transacciones
from .transacciones.crear_transacciones import crear_transaccion
from .transacciones.listar_transacciones import listar_transacciones