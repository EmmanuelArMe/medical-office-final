from sqlalchemy.orm import Session
from app.schemas.horario_medico import HorarioMedicoCreate
from app.models.horario_medico import HorarioMedico
from app.repositories import horario_medico as horario_repository

def crear_horario_medico(db: Session, horario_data: HorarioMedicoCreate):
    horario = HorarioMedico(**horario_data.model_dump())
    return horario_repository.crear_horario_medico(db, horario)

def obtener_horarios(db: Session):
    return horario_repository.obtener_horarios(db)

def obtener_horario_por_id(db: Session, id: int):
    return horario_repository.obtener_horario_por_id(db, id)

def actualizar_horario_medico(db: Session, id: int, data: dict):
    return horario_repository.actualizar_horario_medico(db, id, data)

def eliminar_horario_medico(db: Session, id: int):
    return horario_repository.eliminar_horario_medico(db, id)
