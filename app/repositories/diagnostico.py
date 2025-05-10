from sqlalchemy.orm import Session
from app.models.diagnostico import Diagnostico

def crear_diagnostico(db: Session, diagnostico: Diagnostico):
    db.add(diagnostico)
    db.commit()
    db.refresh(diagnostico)
    return diagnostico

def obtener_diagnostico(db: Session, diagnostico_id: int):
    return db.query(Diagnostico).filter(Diagnostico.id == diagnostico_id).first()

def listar_diagnosticos(db: Session):
    return db.query(Diagnostico).all()

def eliminar_diagnostico(db: Session, diagnostico_id: int):
    diagnostico = obtener_diagnostico(db, diagnostico_id)
    if diagnostico:
        db.delete(diagnostico)
        db.commit()
    return diagnostico
