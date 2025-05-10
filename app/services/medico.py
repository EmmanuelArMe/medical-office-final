from sqlalchemy.orm import Session
from app.schemas.medico import MedicoCreate
from app.models.medico import Medico
from app.repositories import medico as medico_repository

def registrar_medico(db: Session, medico_data: MedicoCreate) -> Medico:
    nuevo_medico = Medico(**medico_data.model_dump())
    return medico_repository.crear_medico(db, nuevo_medico)

def listar_medicos(db: Session) -> list[Medico]:
    return medico_repository.obtener_medicos(db)

def obtener_medico(db: Session, medico_id: int) -> Medico:
    return medico_repository.obtener_medico_por_id(db, medico_id)

def eliminar_medico(db: Session, medico_id: int) -> Medico:
    return medico_repository.eliminar_medico(db, medico_id)