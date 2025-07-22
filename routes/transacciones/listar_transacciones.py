from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
from schemas.transaccion import TransaccionResponse

listar_transacciones_router = APIRouter(prefix="/transacciones", tags=["transacciones"])


@listar_transacciones_router.get("/{id_cuenta}", response_model=List[TransaccionResponse])
def listar_transacciones(id_cuenta: int, db: Session = Depends(get_db)):
    """
    Lista todas las transacciones de una cuenta específica (Art. 219, pág. 219).

    Args:
        id_cuenta: ID de la cuenta.
        db: Sesión de base de datos SQLAlchemy.

    Returns:
        List[TransaccionResponse]: Lista de transacciones.
    """
    try:
        # Verificar existencia de la cuenta
        cuenta = db.query(models.Cuenta).filter(models.Cuenta.id_cuenta == id_cuenta).first()
        if not cuenta:
            raise HTTPException(status_code=404, detail="Cuenta no encontrada")

        transacciones = db.query(models.Transaccion).filter(models.Transaccion.id_cuenta == id_cuenta).all()
        if not transacciones:
            raise HTTPException(status_code=404, detail="No se encontraron transacciones")

        return transacciones
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar transacciones: {str(e)}")