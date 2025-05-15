from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import medicamento as medicamento_repository
from app.models.medicamento import Medicamento
from app.schemas.medicamento import MedicamentoCreate, MedicamentoUpdate

def crear_medicamento(db: Session, medicamento_data: MedicamentoCreate):
    # Validar existencia del medicamento
    medicamento_existente = db.query(Medicamento).filter(Medicamento.nombre == medicamento_data.nombre).first()
    if medicamento_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El medicamento con el nombre {medicamento_data.nombre} ya existe. Por favor, verifique el nombre."
        )
    nuevo_medicamento = medicamento_repository.crear_medicamento(db, medicamento_data)
    if not nuevo_medicamento:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el medicamento"
        )
    return nuevo_medicamento

def obtener_medicamento_por_id(db: Session, medicamento_id: int):
    # Validar existencia del medicamento
    medicamento = db.query(Medicamento).filter(Medicamento.id == medicamento_id).first()
    if not medicamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El medicamento con el id {medicamento_id} no fue encontrado. Por favor, verifique el id."
        )
    return medicamento_repository.obtener_medicamento_por_id(db, medicamento_id)

def obtener_medicamentos(db: Session, skip: int, limit: int):
    # Validar existencia de los medicamentos
    medicamentos = db.query(Medicamento).all()
    if not medicamentos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron medicamentos."
        )
    if skip < 0 or limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los parámetros 'skip' y 'limit' deben ser mayores o iguales a 0 y 1 respectivamente."
        )
    return medicamento_repository.obtener_medicamentos(db, skip=skip, limit=limit)

def eliminar_medicamento(db: Session, medicamento_id: int):
    # Validar existencia del medicamento
    medicamento = obtener_medicamento_por_id(db, medicamento_id)
    medicamento_repository.eliminar_medicamento(db, medicamento_id)
    return medicamento

def actualizar_medicamento(db: Session, medicamento_id: int, medicamento_data: MedicamentoUpdate):
    # Validar existencia del medicamento
    medicamento = obtener_medicamento_por_id(db, medicamento_id)
    # Actualizar el medicamento
    actualizado = medicamento_repository.actualizar_medicamento(db, medicamento, medicamento_data)
    if not actualizado:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al actualizar el medicamento"
        )
    return actualizado