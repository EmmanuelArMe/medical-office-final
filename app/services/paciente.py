from sqlalchemy.orm import Session
from app.repositories import paciente as paciente_repository
from app.schemas.paciente import PacienteCreate

def registrar_paciente(db: Session, paciente: PacienteCreate):
    return paciente_repository.crear_paciente(db, paciente)

def listar_pacientes(db: Session, skip: int = 0, limit: int = 10):
    return paciente_repository.obtener_pacientes(db, skip=skip, limit=limit)

def obtener_paciente(db: Session, documento: int):
    return paciente_repository.obtener_paciente(db, documento=documento)

def eliminar_paciente(db: Session, documento: int):
    return paciente_repository.eliminar_paciente(db, documento=documento)
