from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import pago as pago_repository
from app.models.pago import Pago
from app.schemas.pago import PagoCreate, PagoUpdate
from app.models.paciente import Paciente

def crear_pago(db: Session, pago_data: PagoCreate):
    # Validar existencia del paciente
    paciente = db.query(Paciente).filter(Paciente.id == pago_data.paciente_id).first()
    if not paciente:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El paciente con el id {pago_data.paciente_id} no fue encontrado."
        )
    nuevo_pago = pago_repository.crear_pago(db, pago_data)
    if not nuevo_pago:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el pago"
        )
    return nuevo_pago

def obtener_pago_por_id(db: Session, pago_id: int):
    # Validar existencia del pago
    pago = db.query(Pago).filter(Pago.id == pago_id).first()
    if not pago:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El pago con el id {pago_id} no fue encontrado. Por favor, verifique el id."
        )
    return pago_repository.obtener_pago_por_id(db, pago_id)

def obtener_pagos(db: Session, skip: int, limit: int):
    # Validar existencia de los pagos
    pagos = db.query(Pago).all()
    if not pagos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron pagos."
        )
    if skip < 0 or limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los parámetros 'skip' y 'limit' deben ser mayores o iguales a 0 y 1 respectivamente."
        )
    return pago_repository.obtener_pagos(db, skip=skip, limit=limit)

def eliminar_pago(db: Session, pago_id: int):
    # Validar existencia del pago
    pago = obtener_pago_por_id(db, pago_id)
    pago_repository.eliminar_pago(db, pago_id)
    return pago

def actualizar_pago(db: Session, pago_id: int, pago_data: PagoUpdate):
    # Validar existencia del pago
    pago = obtener_pago_por_id(db, pago_id)
    # Validar existencia del paciente
    paciente = db.query(Paciente).filter(Paciente.id == pago_data.paciente_id).first()
    if not paciente:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El paciente con el id {pago_data.paciente_id} no fue encontrado."
        )
    pago_actualizado = pago_repository.actualizar_pago(db, pago, pago_data)
    if not pago_actualizado:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al actualizar el pago"
        )
    return pago_actualizado

def obtener_pago_por_paciente_id(db: Session, paciente_id: int):
    # Validar existencia del paciente
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron pagos para el paciente con el id {paciente_id}."
        )
    return pago_repository.obtener_pago_por_paciente_id(db, paciente_id)