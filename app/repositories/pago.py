from sqlalchemy.orm import Session
from app.models.pago import Pago
from app.schemas.pago import PagoCreate, PagoUpdate

def crear_pago(db: Session, pago_data: PagoCreate) -> Pago:
    nuevo_pago = Pago(**pago_data.model_dump())
    db.add(nuevo_pago)
    db.commit()
    db.refresh(nuevo_pago)
    return nuevo_pago

def obtener_pago_por_id(db: Session, pago_id: int) -> Pago | None:
    return db.query(Pago).filter(Pago.id == pago_id).first()

def obtener_pagos(db: Session, skip: int, limit: int) -> list[Pago]:
    return db.query(Pago).offset(skip).limit(limit).all()

def eliminar_pago(db: Session, pago_id: int) -> Pago | None:
    pago = obtener_pago_por_id(db, pago_id)
    if pago:
        db.delete(pago)
        db.commit()

def actualizar_pago(db: Session, pago: Pago, pago_data: PagoUpdate) -> Pago | None:
    for key, value in pago_data.model_dump().items():
        setattr(pago, key, value)
    db.commit()
    db.refresh(pago)
    return pago

def obtener_pago_por_paciente_id(db: Session, paciente_id: int) -> Pago | None:
    return db.query(Pago).filter(Pago.paciente_id == paciente_id).first()