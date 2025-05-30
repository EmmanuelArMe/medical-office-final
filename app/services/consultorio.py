from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.consultorio import Consultorio
from app.schemas.consultorio import ConsultorioCreate, ConsultorioUpdate
from app.repositories import consultorio as consultorio_repository

def crear_consultorio(db: Session, consultorio_data: ConsultorioCreate):
    nuevo_consultorio = consultorio_repository.crear_consultorio(db, consultorio_data)
    return nuevo_consultorio

def obtener_consultorio_por_id(db: Session, consultorio_id: int):
    # Validar existencia del consultorio
    consultorio = db.query(Consultorio).filter(Consultorio.id == consultorio_id).first()
    if not consultorio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un consultorio con id {consultorio_id}"
        )
    return consultorio_repository.obtener_consultorio_por_id(db, consultorio_id)

def obtener_consultorios(db: Session, skip: int = 0, limit: int = 10):
    # Validar existencia de consultorios
    consultorios = db.query(Consultorio).all()
    if not consultorios:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron consultorios"
        )
    if skip < 0 or limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los parámetros 'skip' y 'limit' deben ser mayores o iguales a 0 y 1 respectivamente."
        )
    return consultorio_repository.obtener_consultorios(db, skip, limit)


def eliminar_consultorio(db: Session, consultorio_id: int):
    # Validar existencia del consultorio
    consultorio = obtener_consultorio_por_id(db, consultorio_id)
    consultorio_repository.eliminar_consultorio(db, consultorio_id)
    return consultorio

def actualizar_consultorio(db: Session, consultorio_id: int, consultorio_data: ConsultorioUpdate):
    consultorio = obtener_consultorio_por_id(db, consultorio_id)
    consultorio_actualizado = consultorio_repository.actualizar_consultorio(db, consultorio, consultorio_data)
    if not consultorio_actualizado:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al actualizar el consultorio"
        )
    return consultorio_actualizado