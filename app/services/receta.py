from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import receta as receta_repository
from app.models.receta import Receta
from app.models.cita import Cita
from app.schemas.receta import RecetaCreate, RecetaUpdate

def crear_receta(db: Session, receta: RecetaCreate):
    # Validar existencia de la cita
    cita = db.query(Cita).filter(Cita.id == receta.cita_id).first()
    if not cita:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La cita con ID {receta.cita_id} no existe"
        )
    nuevo_receta = receta_repository.crear_receta(db, receta)
    if not nuevo_receta:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el receta"
        )
    return nuevo_receta

def obtener_receta_por_id(db: Session, receta_id: int):
    # Validar existencia de la receta
    receta = db.query(Receta).filter(Receta.id == receta_id).first()
    if not receta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La receta con el id {receta_id} no fue encontrada. Por favor, verifique el id."
        )
    return receta_repository.obtener_receta_por_id(db, receta_id)
    
def obtener_recetas(db: Session, skip: int, limit: int):
    # Validar existencia de las recetas
    recetas = db.query(Receta).all()
    if not recetas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron recetas."
        )
    if skip < 0 or limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los parámetros 'skip' y 'limit' deben ser mayores o iguales a 0 y 1 respectivamente."
        )
    return receta_repository.obtener_recetas(db, skip=skip, limit=limit)

def eliminar_receta(db: Session, receta_id: int):
    # Validar existencia de la receta
    receta = obtener_receta_por_id(db, receta_id)
    receta_repository.eliminar_receta(db, receta_id)
    return receta

def actualizar_receta(db: Session, receta_id: int, receta_data: RecetaUpdate):
    # Validar existencia de la receta
    receta = obtener_receta_por_id(db, receta_id)
    # Validar existencia de la cita
    cita = db.query(Cita).filter(Cita.id == receta_data.cita_id).first()
    if not cita:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La cita con ID {receta_data.cita_id} no existe"
        )
    receta_actualizada = receta_repository.actualizar_receta(db, receta, receta_data)
    if not receta_actualizada:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al actualizar el receta"
        )
    return receta_actualizada

def obtener_recetas_por_cita(db: Session, cita_id: int):
    # Validar existencia de la receta
    receta = db.query(Receta).filter(Receta.cita_id == cita_id).first()
    if not receta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron recetas para la cita con ID {cita_id}."
        )
    return receta_repository.obtener_recetas_por_cita(db, cita_id)
