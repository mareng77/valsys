# schemas/portafolio.py
from pydantic import BaseModel
from datetime import datetime

class PortafolioResponse(BaseModel):
    id_portafolio: int
    id_cuenta: int
    id_activo: int
    cantidad: float
    precio_promedio: float
    fecha_ultima_actualizacion: datetime
    class Config:
        orm_mode = True