from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import receta as receta_repository
from app.models.receta import Receta
from app.schemas.receta import RecetaCreate, RecetaUpdate

def crear_receta(db: Session, receta: RecetaCreate):
    # Validar existencia del receta
    receta_existente = db.query(Receta).filter(Receta.id == receta.id).first()
    if receta_existente:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un receta con el id {id}"
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
    # Validar existencia del receta
    receta = db.query(Receta).filter(Receta.id == receta_id).first()
    if not receta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El receta con el id {receta_id} no fue encontrado. Por favor, verifique el id."
        )
    return receta_repository.obtener_receta_por_id(db, receta_id)
    
def obtener_recetas(db: Session, skip: int, limit: int):
    # Validar existencia de los recetas
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
    # Validar existencia del receta
    receta = obtener_receta_por_id(db, receta_id)
    receta_repository.eliminar_receta(db, receta_id)
    return receta

def actualizar_receta(db: Session, receta_id: int, receta_data: RecetaUpdate):
    # Validar existencia del receta
    receta = obtener_receta_por_id(db, receta_id)
    receta_actualizada = receta_repository.actualizar_receta(db, receta, receta_data)
    if not receta_actualizada:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al actualizar el receta"
        )
    return receta_actualizada
