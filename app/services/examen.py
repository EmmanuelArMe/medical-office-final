from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import examen as examen_repository
from app.models.examen import Examen
from app.schemas.examen import ExamenCreate, ExamenUpdate

def crear_examen(db: Session, examen_data: ExamenCreate):
    # Validar existencia del examen
    examen_existente = db.query(Examen).filter(Examen.nombre == examen_data.nombre).first()
    if examen_existente:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un examen con el nombre {examen_data.nombre}"
        )
    nuevo_examen = examen_repository.crear_examen(db, examen_data)
    if not nuevo_examen:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el examen"
        )
    return nuevo_examen

def obtener_examen_por_id(db: Session, examen_id: int):
    # Validar existencia del examen
    examen = db.query(Examen).filter(Examen.id == examen_id).first()
    if not examen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El examen con el id {examen_id} no fue encontrado. Por favor, verifique el id."
        )
    return examen_repository.obtener_examen_por_id(db, examen_id)

def obtener_examenes(db: Session, skip: int, limit: int):
    # Validar existencia del examen
    examenes = db.query(Examen).all()
    if not examenes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron examenes."
        )
    if skip < 0 or limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los parámetros 'skip' y 'limit' deben ser mayores o iguales a 0 y 1 respectivamente."
        )
    return examen_repository.obtener_examenes(db, skip=skip, limit=limit)

def eliminar_examen(db: Session, examen_id: int):
    # Validar existencia del examen
    examen = obtener_examen_por_id(db, examen_id)
    examen_repository.eliminar_examen(db, examen_id)
    return examen

def actualizar_examen(db: Session, id: int, examen_data: ExamenUpdate) -> Examen | None:
    # Validar existencia del examen
    examen = obtener_examen_por_id(db, id)
    examen_actualizado = examen_repository.actualizar_examen(db, examen, examen_data)
    if not examen_actualizado:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al actualizar el examen"
        )
    return examen_actualizado