from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic_core.core_schema import ValidationInfo

class EmisorCreate(BaseModel):
    nombre: str = Field(..., max_length=100, description="Nombre del emisor")
    tipo_juridico: str = Field(..., max_length=50, description="Tipo jurídico del emisor")

    @field_validator("tipo_juridico", mode="before")
    @classmethod
    def validar_tipo_juridico(cls, v: str) -> str:
        allowed_types = ["Sociedad Anónima", "Cooperativa", "Entidad Pública"]
        if not isinstance(v, str) or v not in allowed_types:
            raise ValueError(f"tipo_juridico debe ser uno de: {', '.join(allowed_types)}")
        return v

class EmisorResponse(BaseModel):
    id_emisor: int
    nombre: str
    tipo_juridico: str
    estado: str
    fecha_registro: datetime

    class Config:
        from_attributes = True

class ProgramaEmisionCreate(BaseModel):
    id_emisor: int = Field(..., gt=0, description="ID del emisor")
    nombre_programa: str = Field(..., max_length=100, description="Nombre del programa")
    monto_autorizado: Decimal = Field(..., ge=0, description="Monto autorizado del programa")
    tipo_valor: str = Field(..., max_length=50, description="Tipo de valor: bonos, acciones, pagarés")
    fecha_vencimiento: Optional[datetime] = Field(None, description="Fecha de vencimiento del programa")
    requiere_calificacion: bool = Field(False, description="Si requiere calificación de riesgo")

    @field_validator("tipo_valor", mode="before")
    @classmethod
    def validar_tipo_valor(cls, v: str) -> str:
        allowed_types = ["bonos", "acciones", "pagarés", "letras de cambio"]
        if not isinstance(v, str) or v not in allowed_types:
            raise ValueError(f"tipo_valor debe ser uno de: {', '.join(allowed_types)}")
        return v

class ProgramaEmisionResponse(BaseModel):
    id_programa: int
    id_emisor: int
    nombre_programa: str
    monto_autorizado: Decimal
    tipo_valor: str
    fecha_inicio: datetime
    fecha_vencimiento: Optional[datetime]
    estado: str
    requiere_calificacion: bool

    class Config:
        from_attributes = True

class ValorCreate(BaseModel):
    id_programa: int = Field(..., gt=0, description="ID del programa de emisión")
    id_activo: Optional[int] = Field(None, description="ID del activo, si aplica")
    descripcion: str = Field(..., max_length=200, description="Descripción del valor")
    monto_emision: Decimal = Field(..., ge=0, description="Monto de la emisión")

class ValorResponse(BaseModel):
    id_valor: int
    id_programa: int
    id_activo: Optional[int]
    descripcion: str
    monto_emision: Decimal
    fecha_emision: datetime
    estado: str

    class Config:
        from_attributes = True