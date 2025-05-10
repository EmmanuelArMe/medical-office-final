from sqlalchemy.orm import Session
from app.repositories import especialidad as especialidad_repository
from app.schemas.especialidad import EspecialidadCreate

def crear_especialidad(db: Session, especialidad_data: EspecialidadCreate):
    return especialidad_repository.crear_especialidad(db, especialidad_data.nombre)

def obtener_especialidades(db: Session):
    return especialidad_repository.obtener_especialidades(db)

def obtener_especialidad_por_id(db: Session, id: int):
    return especialidad_repository.obtener_especialidad_por_id(db, id)

def eliminar_especialidad(db: Session, id: int):
    return especialidad_repository.eliminar_especialidad(db, id)
