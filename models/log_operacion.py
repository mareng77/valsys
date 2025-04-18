# models/log_operacion.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
from datetime import datetime

class LogOperacion(Base):
    __tablename__ = "Logs_Operaciones"
    id_log = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("Usuarios.id_usuario", ondelete="CASCADE"), nullable=False)
    accion = Column(String(255), nullable=False)
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    detalles = Column(String)