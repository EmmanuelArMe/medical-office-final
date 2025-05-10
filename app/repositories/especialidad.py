from sqlalchemy.orm import Session
from app.models.especialidad import Especialidad

def crear_especialidad(db: Session, nombre: str):
    especialidad = Especialidad(nombre=nombre)
    db.add(especialidad)
    db.commit()
    db.refresh(especialidad)
    return especialidad

def obtener_especialidades(db: Session):
    return db.query(Especialidad).all()

def obtener_especialidad_por_id(db: Session, id: int):
    return db.query(Especialidad).filter(Especialidad.id == id).first()

def eliminar_especialidad(db: Session, id: int):
    especialidad = obtener_especialidad_por_id(db, id)
    if especialidad:
        db.delete(especialidad)
        db.commit()
    return especialidad
