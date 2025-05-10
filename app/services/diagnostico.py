from sqlalchemy.orm import Session
from app.schemas.diagnostico import DiagnosticoCreate
from app.models.diagnostico import Diagnostico
from app.repositories import diagnostico as diagnostico_repository

def crear_diagnostico(db: Session, diagnostico_data: DiagnosticoCreate):
    diagnostico = Diagnostico(**diagnostico_data.model_dump())
    return diagnostico_repository.crear_diagnostico(db, diagnostico)

def obtener_diagnostico(db: Session, diagnostico_id: int):
    return diagnostico_repository.obtener_diagnostico(db, diagnostico_id)

def listar_diagnosticos(db: Session):
    return diagnostico_repository.listar_diagnosticos(db)

def eliminar_diagnostico(db: Session, diagnostico_id: int):
    return diagnostico_repository.eliminar_diagnostico(db, diagnostico_id)
