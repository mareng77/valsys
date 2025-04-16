# models/portafolio.py
from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey
from models.base import Base
from datetime import datetime

class Portafolio(Base):
    __tablename__ = "Portafolio"
    id_portafolio = Column(Integer, primary_key=True, index=True)
    id_cuenta = Column(Integer, ForeignKey("Cuentas.id_cuenta", ondelete="CASCADE"), nullable=False)
    id_activo = Column(Integer, ForeignKey("Activos.id_activo", ondelete="CASCADE"), nullable=False)
    cantidad = Column(Numeric(15, 4), nullable=False)
    precio_promedio = Column(Numeric(15, 2), nullable=False)
    fecha_ultima_actualizacion = Column(DateTime, default=datetime.utcnow)