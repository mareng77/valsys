from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Valor(Base):
    __tablename__ = "valores"
    id_valor = Column(Integer, primary_key=True, index=True)
    id_programa = Column(Integer, ForeignKey("programas_emision.id_programa", ondelete="CASCADE"), nullable=False)
    id_activo = Column(Integer, ForeignKey("activos.id_activo"), nullable=True)
    descripcion = Column(String(200), nullable=False)
    monto_emision = Column(Numeric(15, 2), nullable=False)
    fecha_emision = Column(DateTime, default=datetime.utcnow)
    estado = Column(String(20), default="activo")  # activo, redimido
    # Relaciones
    programa = relationship("ProgramaEmision", back_populates="valores")
    __table_args__ = (
        CheckConstraint("estado IN ('activo', 'redimido')", name="valores_estado_check"),
        CheckConstraint("monto_emision >= 0", name="valores_monto_check"),
    )