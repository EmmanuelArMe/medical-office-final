from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import paciente as paciente_repository
from app.models.paciente import Paciente
from app.schemas.paciente import PacienteCreate

def crear_paciente(db: Session, paciente: PacienteCreate):
    # Validar existencia del paciente
    paciente_existente = db.query(Paciente).filter(Paciente.documento == paciente.documento).first()
    if paciente_existente:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un paciente con el documento {paciente.documento}"
        )
    nuevo_paciente = paciente_repository.crear_paciente(db, paciente)
    if not nuevo_paciente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el paciente"
        )
    return nuevo_paciente

def listar_pacientes(db: Session, skip: int = 0, limit: int = 10):
    return paciente_repository.obtener_pacientes(db, skip=skip, limit=limit)

def obtener_paciente(db: Session, documento: int):
    return paciente_repository.obtener_paciente(db, documento=documento)

def eliminar_paciente(db: Session, documento: int):
    return paciente_repository.eliminar_paciente(db, documento=documento)
