from sqlalchemy.orm import Session
from app.models.historial_medico import HistorialMedico

def obtener_todos(db: Session):
    return db.query(HistorialMedico).all()

def obtener_por_id(db: Session, id: int):
    return db.query(HistorialMedico).filter(HistorialMedico.id == id).first()

def crear(db: Session, historial_data: dict):
    historial = HistorialMedico(**historial_data)
    db.add(historial)
    db.commit()
    db.refresh(historial)
    return historial

def actualizar(db: Session, id: int, historial_data: dict):
    historial = obtener_por_id(db, id)
    if historial:
        for key, value in historial_data.items():
            setattr(historial, key, value)
        db.commit()
        db.refresh(historial)
    return historial

def eliminar(db: Session, id: int):
    historial = obtener_por_id(db, id)
    if historial:
        db.delete(historial)
        db.commit()
        return historial
    return None
