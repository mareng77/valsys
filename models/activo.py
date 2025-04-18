# models/activo.py
from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Activo(Base):
    __tablename__ = "activos"
    id_activo = Column(Integer, primary_key=True, index=True)
    tipo_activo = Column(String(50), nullable=False)
    nombre_activo = Column(String(255), nullable=False)
    ticker = Column(String(20), unique=True, nullable=False)
    precio_actual = Column(Numeric(15, 2), nullable=False)
    mercado = Column(String(100), nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow)
    portafolios = relationship("Portafolio", back_populates="activo")
    #transacciones = relationship("Transaccion", back_populates="activo")