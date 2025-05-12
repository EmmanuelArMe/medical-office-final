from sqlalchemy.orm import Session
from app.models.especialidad import Especialidad
from app.schemas.especialidad import EspecialidadCreate
from app.schemas.especialidad import EspecialidadCreate

def crear_especialidad(db: Session, especialidad_data: EspecialidadCreate) -> Especialidad:
    nueva_especialidad = Especialidad(**especialidad_data.model_dump())
    db.add(nueva_especialidad)
    db.commit()
    db.refresh(nueva_especialidad)
    return nueva_especialidad

def obtener_especialidad_por_id(db: Session, especialidad_id: int) -> Especialidad | None:
    return db.query(Especialidad).filter(Especialidad.id == especialidad_id).first()

def obtener_especialidades(db: Session, skip: int, limit: int) -> list[Especialidad]:
    return db.query(Especialidad).offset(skip).limit(limit).all()

def eliminar_especialidad(db: Session, especialidad_id: int) -> Especialidad | None:
    especialidad = obtener_especialidad_por_id(db, especialidad_id)
    if especialidad:
        db.delete(especialidad)
        db.commit()
    return especialidad

def actualizar_especialidad(db: Session, especialidad_id: int, especialidad_data: EspecialidadCreate) -> Especialidad | None:
    especialidad = obtener_especialidad_por_id(db, especialidad_id)
    if especialidad:
        for key, value in especialidad_data.model_dump().items():
            setattr(especialidad, key, value)
        db.commit()
        db.refresh(especialidad)
    return especialidad
