# models/associations.py
from sqlalchemy import Table, Column, Integer, ForeignKey
from models.base import Base

usuario_roles = Table(
    "usuario_roles",
    Base.metadata,
    Column("id_usuario", Integer, ForeignKey("usuarios.id_usuario"), primary_key=True),
    Column("id_rol", Integer, ForeignKey("roles.id_rol"), primary_key=True)
)