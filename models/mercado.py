# models/mercado.py
from sqlalchemy import Column, Integer, String, Time
from models.base import Base

class Mercado(Base):
    __tablename__ = "Mercados"
    id_mercado = Column(Integer, primary_key=True, index=True)
    nombre_mercado = Column(String(255), nullable=False)
    pais = Column(String(100))
    moneda_base = Column(String(3), nullable=False)
    horario_apertura = Column(Time)
    horario_cierre = Column(Time)