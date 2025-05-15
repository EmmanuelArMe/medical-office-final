from sqlalchemy.orm import Session
from app.models.historial_medico import HistorialMedico
from app.schemas.historial_medico import HistorialMedicoCreate, HistorialMedicoUpdate

def crear_historial_medico(db: Session, historial: HistorialMedicoCreate):
    nuevo_historial_medico = HistorialMedico(**historial.model_dump())
    db.add(nuevo_historial_medico)
    db.commit()
    db.refresh(nuevo_historial_medico)
    return nuevo_historial_medico


def obtener_historial_medico_por_id(db: Session, id: int):
    return db.query(HistorialMedico).filter(HistorialMedico.id == id).first()

def obtener_historiales_medicos(db: Session, skip: int, limit: int):
    return db.query(HistorialMedico).offset(skip).limit(limit).all()

def eliminar_historial_medico(db: Session, id: int):
    historial = obtener_historial_medico_por_id(db, id)
    if historial:
        db.delete(historial)
        db.commit()

def actualizar_historial_medico(db: Session, id: int, historial: HistorialMedico, historial_data: HistorialMedicoUpdate) -> HistorialMedico | None:
    for key, value in historial_data.items():
        setattr(historial, key, value)
    db.commit()
    db.refresh(historial)
    return historial

def obtener_historiales_medicos_por_id_paciente(db: Session, paciente_id: int):
    return db.query(HistorialMedico).filter(HistorialMedico.paciente_id == paciente_id).all()
