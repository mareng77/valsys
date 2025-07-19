from pydantic import BaseModel, Field, validator
from datetime import datetime
from decimal import Decimal
from typing import Optional

class TransaccionCreate(BaseModel):
    id_cuenta: int = Field(..., gt=0, description="ID de la cuenta asociada")
    id_activo: Optional[int] = Field(None, description="ID del activo, si aplica")
    tipo_transaccion: str = Field(..., description="Tipo de transacción: compra, venta, deposito o retiro")
    monto: Decimal = Field(..., ge=0, description="Monto total de la transacción")  # ge=0 para transacciones_monto_check
    cantidad: Optional[Decimal] = Field(None, ge=0, description="Cantidad de activos")
    precio_unitario: Optional[Decimal] = Field(None, gt=0, description="Precio unitario por activo")

    @validator("tipo_transaccion")
    def validar_tipo_transaccion(cls, v):
        allowed_types = ["compra", "venta", "deposito", "retiro"]
        if v.lower() not in allowed_types:
            raise ValueError(f"tipo_transaccion debe ser uno de: {', '.join(allowed_types)}")
        return v.lower()

    @validator("monto")
    def validar_monto(cls, v, values):
        if "cantidad" in values and values["cantidad"] is not None and \
           "precio_unitario" in values and values["precio_unitario"] is not None:
            if abs(v - values["cantidad"] * values["precio_unitario"]) > Decimal("0.01"):
                raise ValueError("El monto debe ser igual a cantidad * precio_unitario")
        return v

class TransaccionResponse(BaseModel):
    id_transaccion: int
    id_cuenta: int
    id_activo: Optional[int]
    tipo_transaccion: str
    monto: Decimal
    cantidad: Optional[Decimal]
    precio_unitario: Optional[Decimal]
    fecha_transaccion: datetime
    estado: str

    class Config:
        from_attributes = True