# models/cuenta.py
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
from datetime import datetime

class Cuenta(Base):
    __tablename__ = "cuentas"
    id_cuenta = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="CASCADE"), nullable=False)
    saldo_disponible = Column(Numeric(15, 2), default=0.00)
    moneda = Column(String(3), nullable=False)
    estado = Column(String(20), default="activa")
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    usuario = relationship("Usuario", back_populates="cuentas")
    ordenes = relationship("Orden", back_populates="cuenta")
