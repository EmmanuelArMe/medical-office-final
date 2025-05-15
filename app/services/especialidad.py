from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import especialidad as especialidad_repository
from app.schemas.especialidad import EspecialidadCreate , EspecialidadUpdate
from app.models.especialidad import Especialidad

def crear_especialidad(db: Session, especialidad_data: EspecialidadCreate):
    # Validar existencia de la especialidad
    especialidad_existente = db.query(especialidad_repository.Especialidad).filter(
        especialidad_repository.Especialidad.nombre == especialidad_data.nombre
    ).first()
    if especialidad_existente:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una especialidad con el nombre {especialidad_data.nombre}"
        )
    nueva_especialidad = especialidad_repository.crear_especialidad(db, especialidad_data)
    if not nueva_especialidad:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear la especialidad"
        )
    
    return nueva_especialidad

def obtener_especialidad_por_id(db: Session, id: int):
    # Validar existencia de la especialidad
    especialidad = db.query(Especialidad).filter(Especialidad.id == id).first()
    if not especialidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La especialidad con el id {id} no fue encontrada. Por favor, verifique el id."
        )
    return especialidad_repository.obtener_especialidad_por_id(db, id)

def obtener_especialidades(db: Session, skip: int, limit: int):
    # Validar existencia de la especialidad
    especialidades = db.query(especialidad_repository.Especialidad).all()
    if not especialidades:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron especialidades."
        )
    if skip < 0 or limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los parámetros 'skip' y 'limit' deben ser mayores o iguales a 0 y 1 respectivamente."
        )
    return especialidad_repository.obtener_especialidades(db, skip=skip, limit=limit)

def eliminar_especialidad(db: Session, id: int):
    # Validar existencia de la especialidad
    especialidad = obtener_especialidad_por_id(db, id)
    especialidad_repository.eliminar_especialidad(db, id)
    return especialidad

def actualizar_especialidad(db: Session, id: int, especialidad_data: EspecialidadUpdate):
    # Validar existencia de la especialidad
    especialidad = obtener_especialidad_por_id(db, id)
    especialidad_actualizada = especialidad_repository.actualizar_especialidad(db, especialidad, especialidad_data)
    if not especialidad_actualizada:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al actualizar la especialidad"
        )
    return especialidad_actualizada