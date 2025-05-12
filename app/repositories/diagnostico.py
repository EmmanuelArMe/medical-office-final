from sqlalchemy.orm import Session
from app.models.diagnostico import Diagnostico
from app.schemas.diagnostico import DiagnosticoCreate

def crear_diagnostico(db: Session, diagnostico_data: DiagnosticoCreate) -> Diagnostico:
    nuevo_diagnostico = Diagnostico(**diagnostico_data.model_dump())
    db.add(nuevo_diagnostico)
    db.commit()
    db.refresh(nuevo_diagnostico)
    return nuevo_diagnostico

def obtener_diagnostico(db: Session, diagnostico_id: int) -> Diagnostico | None:
    return db.query(Diagnostico).filter(Diagnostico.id == diagnostico_id).first()

def obtener_diagnosticos(db: Session, skip: int, limit: int) -> list[Diagnostico]:
    return db.query(Diagnostico).offset(skip).limit(limit).all()

def eliminar_diagnostico(db: Session, diagnostico_id: int):
    diagnostico = obtener_diagnostico(db, diagnostico_id)
    if diagnostico:
        db.delete(diagnostico)
        db.commit()
    return diagnostico

"""
def actualizar_diagnostico(db: Session, diagnostico_id: int, diagnostico_data: DiagnosticoUpdate) -> Diagnostico | None:
    diagnostico = obtener_diagnostico(db, diagnostico_id)
    if diagnostico:
        for key, value in diagnostico_data.model_dump().items():
            setattr(diagnostico, key, value)
        db.commit()
        db.refresh(diagnostico)
    return diagnostico
"""