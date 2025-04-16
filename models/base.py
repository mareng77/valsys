# models/base.py
from sqlalchemy import Table, Column, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

usuario_roles = Table(
    'Usuario_Roles', Base.metadata,
    Column('id_usuario', Integer, ForeignKey('Usuarios.id_usuario', ondelete='CASCADE'), primary_key=True),
    Column('id_rol', Integer, ForeignKey('Roles.id_rol', ondelete='CASCADE'), primary_key=True),
    Column('fecha_asignacion', DateTime, default=datetime.utcnow)
)