from pydantic import BaseModel

class ActivoCreate(BaseModel):
    tipo_activo: str
    nombre_activo: str
    ticker: str
    precio_actual: float
    mercado: str

class ActivoResponse(BaseModel):
    id_activo: int
    nombre_activo: str
    ticker: str
    precio_actual: float
    tipo_activo: str