# models/transaccion.py
from datetime import datetime
from database import Base
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey


class Transaccion(Base):
    __tablename__ = "transacciones"
    id_transaccion = Column(Integer, primary_key=True, index=True)
    id_cuenta = Column(Integer, ForeignKey("cuentas.id_cuenta", ondelete="CASCADE"), nullable=False)
    id_activo = Column(Integer, ForeignKey("activos.id_activo"), nullable=True)
    tipo_transaccion = Column(String(20), nullable=False)
    monto = Column(Numeric(15, 2), nullable=False)
    cantidad = Column(Numeric(15, 4))
    precio_unitario = Column(Numeric(15, 2))
    fecha_transaccion = Column(DateTime, default=datetime.utcnow)
    estado = Column(String(20), default="pendiente")
    #cuenta = relationship("Cuenta", back_populates="transacciones")
    #activo = relationship("Activo", back_populates="transacciones")