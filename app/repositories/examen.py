from sqlalchemy.orm import Session
from app.models.examen import Examen
from app.schemas.examen import ExamenCreate, ExamenUpdate

def crear_examen(db: Session, examen_data: ExamenCreate) -> Examen:
    nuevo_examen = Examen(**examen_data.model_dump())
    db.add(nuevo_examen)
    db.commit()
    db.refresh(nuevo_examen)
    return nuevo_examen

def obtener_examen_por_id(db: Session, examen_id: int) -> Examen | None:
    return db.query(Examen).filter(Examen.id == examen_id).first()

def obtener_examenes(db: Session, skip: int, limit: int) -> list[Examen]:
    return db.query(Examen).offset(skip).limit(limit).all()

def eliminar_examen(db: Session, examen_id: int) -> Examen | None:
    examen = obtener_examen_por_id(db, examen_id)
    if examen:
        db.delete(examen)
        db.commit()

def actualizar_examen(db: Session, examen: Examen, examen_data: ExamenUpdate) -> Examen | None:
    for key, value in examen_data.model_dump().items():
        setattr(examen, key, value)
    db.commit()
    db.refresh(examen)
    return examen