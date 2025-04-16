# schemas/cuenta.py
from pydantic import BaseModel
from typing import Optional

class CuentaCreate(BaseModel):
    id_usuario: int
    saldo_disponible: float = 0.00
    moneda: str
    estado: str = "activa"

class CuentaResponse(BaseModel):
    id_cuenta: int
    id_usuario: int
    saldo_disponible: float
    moneda: str
    estado: str
    fecha_creacion: Optional[str] = None

    class Config:
        from_attributes = True