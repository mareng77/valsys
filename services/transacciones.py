# services/transacciones.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import Cuenta, Activo, Transaccion
from schemas.transaccion import TransaccionCreate

def validar_y_crear_transaccion(db: Session, transaccion: TransaccionCreate):
    cuenta = db.query(Cuenta).filter(Cuenta.id_cuenta == transaccion.id_cuenta).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")

    if transaccion.tipo_transaccion in ["compra", "venta"]:
        if transaccion.id_activo is None:
            raise HTTPException(status_code=400, detail="Se requiere un id_activo para compra o venta")
        activo = db.query(Activo).filter(Activo.id_activo == transaccion.id_activo).first()
        if not activo:
            raise HTTPException(status_code=404, detail="Activo no encontrado")

    db_transaccion = Transaccion(
        id_cuenta=transaccion.id_cuenta,
        id_activo=transaccion.id_activo,
        tipo_transaccion=transaccion.tipo_transaccion,
        monto=transaccion.monto,
        cantidad=transaccion.cantidad,
        precio_unitario=transaccion.precio_unitario
    )
    db.add(db_transaccion)
    db.commit()
    db.refresh(db_transaccion)
    return db_transaccion

def obtener_transacciones_por_cuenta(db: Session, id_cuenta: int):
    transacciones = db.query(Transaccion).filter(Transaccion.id_cuenta == id_cuenta).all()
    return [{"id_transaccion": t.id_transaccion, "tipo_transaccion": t.tipo_transaccion, "monto": t.monto, "fecha": t.fecha_transaccion} for t in transacciones]