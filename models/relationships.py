# models/relationships.py
from sqlalchemy.orm import relationship
from .cuenta import Cuenta
from .orden import Orden
from .activo import Activo

def configure_relationships():
    # Relaciones para Cuenta
    Cuenta.ordenes = relationship("Orden", back_populates="cuenta")

    # Relaciones para Orden
    Orden.cuenta = relationship("Cuenta", back_populates="ordenes")
    Orden.activo = relationship("Activo", back_populates="ordenes")

    # Relaciones para Activo
    Activo.ordenes = relationship("Orden", back_populates="activo")