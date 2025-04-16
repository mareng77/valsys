from pydantic import BaseModel
from typing import Literal, Union

class TransaccionCreate(BaseModel):
    id_cuenta: int
    id_activo: Union[int, None] = None
    tipo_transaccion: Literal["compra", "venta", "deposito", "retiro"]
    monto: float
    cantidad: Union[float, None] = None
    precio_unitario: Union[float, None] = None