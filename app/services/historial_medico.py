from sqlalchemy.orm import Session
from app.repositories import historial_medico as historial_medico_repository
from app.schemas.historial_medico import HistorialMedicoCreate, HistorialMedicoUpdate

def obtener_historiales(db: Session):
    return historial_medico_repository.obtener_todos(db)

def obtener_historial(db: Session, id: int):
    return historial_medico_repository.obtener_por_id(db, id)

def crear_historial(db: Session, historial: HistorialMedicoCreate):
    return historial_medico_repository.crear(db, historial.dict())

def actualizar_historial(db: Session, id: int, historial: HistorialMedicoUpdate):
    return historial_medico_repository.actualizar(db, id, historial.dict())

def eliminar_historial(db: Session, id: int):
    return historial_medico_repository.eliminar(db, id)
