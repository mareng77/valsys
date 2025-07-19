from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class ProgramaEmision(Base):
    __tablename__ = "programas_emision"
    id_programa = Column(Integer, primary_key=True, index=True)
    id_emisor = Column(Integer, ForeignKey("emisores.id_emisor", ondelete="CASCADE"), nullable=False)
    nombre_programa = Column(String(100), nullable=False)
    monto_autorizado = Column(Numeric(15, 2), nullable=False)
    tipo_valor = Column(String(50), nullable=False)  # Ej: 'bonos', 'acciones', 'pagarés'
    fecha_inicio = Column(DateTime, default=datetime.utcnow)
    fecha_vencimiento = Column(DateTime, nullable=True)
    estado = Column(String(20), default="activo")  # activo, finalizado, suspendido
    requiere_calificacion = Column(Boolean, default=False)
    # Relaciones
    emisor = relationship("Emisor", back_populates="programas")
    valores = relationship("Valor", back_populates="programa")
    __table_args__ = (
        CheckConstraint("estado IN ('activo', 'finalizado', 'suspendido')", name="programas_emision_estado_check"),
        CheckConstraint("monto_autorizado >= 0", name="programas_emision_monto_check"),
    )