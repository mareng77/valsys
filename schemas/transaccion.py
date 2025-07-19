from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic_core.core_schema import ValidationInfo

class TransaccionCreate(BaseModel):
    id_cuenta: int = Field(..., gt=0, description="ID de la cuenta asociada")
    id_activo: Optional[int] = Field(None, description="ID del activo, si aplica")
    tipo_transaccion: str = Field(..., description="Tipo de transacción: compra, venta, deposito o retiro")
    monto: Decimal = Field(..., ge=0, description="Monto total de la transacción")
    cantidad: Optional[Decimal] = Field(None, ge=0, description="Cantidad de activos")
    precio_unitario: Optional[Decimal] = Field(None, gt=0, description="Precio unitario por activo")

    @field_validator("tipo_transaccion", mode="before")
    @classmethod
    def validar_tipo_transaccion(cls, v: str) -> str:
        allowed_types = ["compra", "venta", "deposito", "retiro"]
        if not isinstance(v, str) or v.lower() not in allowed_types:
            raise ValueError(f"tipo_transaccion debe ser uno de: {', '.join(allowed_types)}")
        return v.lower()

    @field_validator("monto", mode="before")
    @classmethod
    def validar_monto(cls, v: Decimal, info: ValidationInfo) -> Decimal:
        if "cantidad" in info.data and info.data["cantidad"] is not None and \
           "precio_unitario" in info.data and info.data["precio_unitario"] is not None:
            if abs(v - info.data["cantidad"] * info.data["precio_unitario"]) > Decimal("0.01"):
                raise ValueError("El monto debe ser igual a cantidad * precio_unitario")
        return v

    @field_validator("id_activo", "cantidad", "precio_unitario", mode="before")
    @classmethod
    def validar_campos_compra_venta(cls, v: any, info: ValidationInfo) -> any:
        tipo_transaccion = info.data.get("tipo_transaccion")
        if tipo_transaccion:
            if tipo_transaccion in ["deposito", "retiro"] and v is not None:
                raise ValueError(f"{info.field_name} debe ser nulo para deposito o retiro")
            if tipo_transaccion in ["compra", "venta"] and v is None:
                raise ValueError(f"{info.field_name} es obligatorio para compra o venta")
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