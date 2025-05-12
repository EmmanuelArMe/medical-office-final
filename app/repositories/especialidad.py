from sqlalchemy.orm import Session
from app.models.especialidad import Especialidad
from app.schemas.especialidad import EspecialidadCreate

def crear_especialidad(db: Session, especialidad: EspecialidadCreate):
    especialidad = Especialidad(**especialidad.model_dump())
    db.add(especialidad)
    db.commit()
    db.refresh(especialidad)
    return especialidad

def obtener_especialidad_por_id(db: Session, id: int):
    return db.query(Especialidad).filter(Especialidad.id == id).first()

def obtener_especialidades(db: Session, skip: int, limit: int):
    return db.query(Especialidad).offset(skip).limit(limit).all()

def eliminar_especialidad(db: Session, id: int):
    especialidad = obtener_especialidad_por_id(db, id)
    if especialidad:
        db.delete(especialidad)
        db.commit()

def actualizar_especialidad(db: Session, especialidad: Especialidad, especialidad_data: EspecialidadCreate) -> Especialidad | None:
    for key, value in especialidad_data.model_dump().items():
        setattr(especialidad, key, value)
    db.commit()
    db.refresh(especialidad)
    return especialidad
