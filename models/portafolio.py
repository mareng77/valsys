# models/portafolio.py
from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Portafolio(Base):
    __tablename__ = "portafolio"
    id_portafolio = Column(Integer, primary_key=True, index=True)
    id_cuenta = Column(Integer, ForeignKey("cuentas.id_cuenta", ondelete="CASCADE"), nullable=False)
    id_activo = Column(Integer, ForeignKey("activos.id_activo", ondelete="CASCADE"), nullable=False)
    cantidad = Column(Numeric(15, 4), nullable=False)
    precio_promedio = Column(Numeric(15, 2), nullable=False)
    fecha_ultima_actualizacion = Column(DateTime, default=datetime.utcnow)
    #cuenta = relationship("Cuenta", back_populates="portafolios")
    #activo = relationship("Activo", back_populates="portafolios")
