from sqlalchemy.orm import Session
from app.models.medico import Medico

def crear_medico(db: Session, medico: Medico) -> Medico:
    db.add(medico)
    db.commit()
    db.refresh(medico)
    return medico

def obtener_medico_por_id(db: Session, medico_id: int) -> Medico:
    return db.query(Medico).filter(Medico.id == medico_id).first()

def obtener_medicos(db: Session) -> list[Medico]:
    return db.query(Medico).all()

def eliminar_medico(db: Session, medico_id: int) -> Medico:
    medico = obtener_medico_por_id(db, medico_id)
    if medico:
        db.delete(medico)
        db.commit()
    return medico