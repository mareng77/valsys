from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from decimal import Decimal
from database import get_db
import models
from schemas.transaccion import TransaccionCreate, TransaccionResponse

crear_transacciones_router = APIRouter(prefix="/transacciones", tags=["transacciones"])


@crear_transacciones_router.post("/", response_model=TransaccionResponse)
def crear_transaccion(transaccion: TransaccionCreate, db: Session = Depends(get_db)):
    """
    Crea una transacción de compra/venta/deposito/retiro (Art. 21, 219, pág. 21, 219).

    Args:
        transaccion: Esquema con datos de la transacción.
        db: Sesión de base de datos SQLAlchemy.

    Returns:
        TransaccionResponse: Detalles de la transacción creada.
    """
    try:
        # Verificar existencia de la cuenta
        cuenta = db.query(models.Cuenta).filter(models.Cuenta.id_cuenta == transaccion.id_cuenta).first()
        if not cuenta:
            raise HTTPException(status_code=404, detail="Cuenta no encontrada")

        # Verificar elegibilidad de la cuenta (Art. 6, pág. 2)
        if cuenta.estado.lower() != "activa" or cuenta.moneda not in ["PYG", "USD"]:
            raise HTTPException(status_code=400, detail="Cuenta no elegible para operar")

        # Verificar saldo para compras y retiros
        if transaccion.tipo_transaccion in ["compra", "retiro"] and cuenta.saldo_disponible < transaccion.monto:
            raise HTTPException(status_code=400, detail="Saldo insuficiente")

        # Verificar existencia del activo para compras y ventas
        if transaccion.tipo_transaccion in ["compra", "venta"]:
            if transaccion.id_activo:
                activo = db.query(models.Activo).filter(models.Activo.id_activo == transaccion.id_activo).first()
                if not activo:
                    raise HTTPException(status_code=404, detail="Activo no encontrado")
            # Verificar que el activo esté vinculado a un valor activo
            valor = db.query(models.Valor).filter(models.Valor.id_activo == transaccion.id_activo,
                                                  models.Valor.estado == "activo").first()
            if not valor:
                raise HTTPException(status_code=400, detail="Activo no vinculado a un valor activo")

        # Actualizar saldo de la cuenta
        if transaccion.tipo_transaccion == "compra":
            cuenta.saldo_disponible -= transaccion.monto
        elif transaccion.tipo_transaccion == "venta":
            cuenta.saldo_disponible += transaccion.monto
        elif transaccion.tipo_transaccion == "deposito":
            cuenta.saldo_disponible += transaccion.monto
        elif transaccion.tipo_transaccion == "retiro":
            cuenta.saldo_disponible -= transaccion.monto

        # Crear transacción
        db_transaccion = models.Transaccion(
            id_cuenta=transaccion.id_cuenta,
            id_activo=transaccion.id_activo,
            tipo_transaccion=transaccion.tipo_transaccion,
            monto=transaccion.monto,
            cantidad=transaccion.cantidad,
            precio_unitario=transaccion.precio_unitario,
            fecha_transaccion=datetime.utcnow(),
            estado="pendiente"
        )

        db.add(db_transaccion)
        db.commit()
        db.refresh(cuenta)
        db.refresh(db_transaccion)

        return db_transaccion
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear transacción: {str(e)}")