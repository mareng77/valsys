from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from decimal import Decimal
from database import get_db
import models
from schemas.emision import EmisorCreate, EmisorResponse, ProgramaEmisionCreate, ProgramaEmisionResponse, ValorCreate, \
    ValorResponse

emision_router = APIRouter(prefix="/emision", tags=["emissions"])


@emision_router.post("/emisores/", response_model=EmisorResponse)
def crear_emisor(emisor: EmisorCreate, db: Session = Depends(get_db)):
    """
    Crea un emisor para programas de emisión (Art. 14, Ley 5810/2017).
    """
    try:
        db_emisor = models.Emisor(
            nombre=emisor.nombre,
            tipo_juridico=emisor.tipo_juridico,
            estado="activo",
            fecha_registro=datetime.utcnow()
        )
        db.add(db_emisor)
        db.commit()
        db.refresh(db_emisor)
        return db_emisor
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear emisor: {str(e)}")


@emision_router.get("/emisores/{id_emisor}", response_model=EmisorResponse)
def obtener_emisor(id_emisor: int, db: Session = Depends(get_db)):
    """
    Obtiene un emisor por ID.
    """
    emisor = db.query(models.Emisor).filter(models.Emisor.id_emisor == id_emisor).first()
    if not emisor:
        raise HTTPException(status_code=404, detail="Emisor no encontrado")
    return emisor


@emision_router.post("/programas/", response_model=ProgramaEmisionResponse)
def crear_programa_emision(programa: ProgramaEmisionCreate, db: Session = Depends(get_db)):
    """
    Crea un programa de emisión global (pág. 219, Reglamento).
    """
    try:
        # Verificar emisor
        emisor = db.query(models.Emisor).filter(models.Emisor.id_emisor == programa.id_emisor).first()
        if not emisor:
            raise HTTPException(status_code=404, detail="Emisor no encontrado")
        if emisor.estado != "activo":
            raise HTTPException(status_code=400, detail="Emisor no activo")

        db_programa = models.ProgramaEmision(
            id_emisor=programa.id_emisor,
            nombre_programa=programa.nombre_programa,
            monto_autorizado=programa.monto_autorizado,
            tipo_valor=programa.tipo_valor,
            fecha_inicio=datetime.utcnow(),
            fecha_vencimiento=programa.fecha_vencimiento,
            estado="activo",
            requiere_calificacion=programa.requiere_calificacion
        )
        db.add(db_programa)
        db.commit()
        db.refresh(db_programa)
        return db_programa
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear programa: {str(e)}")


@emision_router.get("/programas/{id_programa}", response_model=ProgramaEmisionResponse)
def obtener_programa(id_programa: int, db: Session = Depends(get_db)):
    """
    Obtiene un programa de emisión por ID.
    """
    programa = db.query(models.ProgramaEmision).filter(models.ProgramaEmision.id_programa == id_programa).first()
    if not programa:
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    return programa


@emision_router.post("/valores/", response_model=ValorResponse)
def crear_valor(valor: ValorCreate, db: Session = Depends(get_db)):
    """
    Crea un valor bajo un programa de emisión (Art. 69, Ley 5810/2017).
    """
    try:
        # Verificar programa
        programa = db.query(models.ProgramaEmision).filter(
            models.ProgramaEmision.id_programa == valor.id_programa).first()
        if not programa:
            raise HTTPException(status_code=404, detail="Programa no encontrado")
        if programa.estado != "activo":
            raise HTTPException(status_code=400, detail="Programa no activo")

        # Verificar activo, si aplica
        if valor.id_activo:
            activo = db.query(models.Activo).filter(models.Activo.id_activo == valor.id_activo).first()
            if not activo:
                raise HTTPException(status_code=404, detail="Activo no encontrado")

        # Verificar monto autorizado
        valores_existentes = db.query(models.Valor).filter(models.Valor.id_programa == valor.id_programa).all()
        monto_total = sum(v.monto_emision for v in valores_existentes) + valor.monto_emision
        if monto_total > programa.monto_autorizado:
            raise HTTPException(status_code=400, detail="Monto excede el autorizado")

        db_valor = models.Valor(
            id_programa=valor.id_programa,
            id_activo=valor.id_activo,
            descripcion=valor.descripcion,
            monto_emision=valor.monto_emision,
            fecha_emision=datetime.utcnow(),
            estado="activo"
        )
        db.add(db_valor)
        db.commit()
        db.refresh(db_valor)
        return db_valor
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear valor: {str(e)}")


@emision_router.get("/valores/{id_programa}", response_model=List[ValorResponse])
def listar_valores(id_programa: int, db: Session = Depends(get_db)):
    """
    Lista los valores de un programa de emisión.
    """
    valores = db.query(models.Valor).filter(models.Valor.id_programa == id_programa).all()
    if not valores:
        raise HTTPException(status_code=404, detail="No se encontraron valores")
    return valores