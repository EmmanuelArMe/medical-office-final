from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import especialidad as especialidad_repository
from app.schemas.especialidad import EspecialidadCreate

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

def obtener_especialidades(db: Session):
    return especialidad_repository.obtener_especialidades(db)

def obtener_especialidad_por_id(db: Session, id: int):
    return especialidad_repository.obtener_especialidad_por_id(db, id)

def eliminar_especialidad(db: Session, id: int):
    return especialidad_repository.eliminar_especialidad(db, id)
