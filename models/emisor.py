from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Emisor(Base):
    __tablename__ = "emisores"
    id_emisor = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    tipo_juridico = Column(String(50), nullable=False)  # Ej: 'Sociedad Anónima', 'Cooperativa'
    estado = Column(String(20), default="activo")  # activo, suspendido
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    # Relaciones
    programas = relationship("ProgramaEmision", back_populates="emisor")
    __table_args__ = (
        CheckConstraint("estado IN ('activo', 'suspendido')", name="emisores_estado_check"),
    )