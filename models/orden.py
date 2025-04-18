# models/orden.py
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Orden(Base):
    __tablename__ = "ordenes"
    id_orden = Column(Integer, primary_key=True, index=True)
    id_cuenta = Column(Integer, ForeignKey("cuentas.id_cuenta", ondelete="CASCADE"), nullable=False)
    id_activo = Column(Integer, ForeignKey("activos.id_activo", ondelete="CASCADE"), nullable=False)
    tipo = Column(String(10), nullable=False)
    cantidad = Column(Numeric(15, 4), nullable=False)
    precio_limite = Column(Numeric(15, 2), nullable=False)
    estado = Column(String(20), nullable=False, default="pendiente")
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    cuenta = relationship("Cuenta", back_populates="ordenes")
    activo = relationship("Activo", back_populates="ordenes")