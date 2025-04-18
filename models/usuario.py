# models/usuario.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

# Define the usuario_roles table
usuario_roles = Table(
    "usuario_roles",
    Base.metadata,
    Column("id_usuario", Integer, ForeignKey("usuarios.id_usuario", ondelete="CASCADE"), primary_key=True),
    Column("id_rol", Integer, ForeignKey("roles.id_rol", ondelete="CASCADE"), primary_key=True),
    Column("fecha_asignacion", DateTime, default=datetime.utcnow)
)

class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    contraseña_hash = Column(String(255), nullable=False)
    telefono = Column(String(20))
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    activo = Column(Boolean, default=True)
    cuentas = relationship("Cuenta", back_populates="usuario")
    roles = relationship("Rol", secondary=usuario_roles, back_populates="usuarios")