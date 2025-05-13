from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import paciente as paciente_repository
from app.models.paciente import Paciente
from app.schemas.paciente import PacienteCreate, PacienteUpdate

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
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el paciente"
        )
    return nuevo_paciente

def obtener_paciente_por_documento(db: Session, documento: int):
    # Validar existencia del paciente
    paciente = db.query(Paciente).filter(Paciente.documento == documento).first()
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El paciente con el documento {documento} no fue encontrado. Por favor, verifique el documento."
        )
    return paciente_repository.obtener_paciente_por_documento(db, documento=documento)
    
def obtener_pacientes(db: Session, skip: int, limit: int):
    # Validar existencia de los pacientes
    pacientes = db.query(Paciente).all()
    if not pacientes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron pacientes."
        )
    if skip < 0 or limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los parámetros 'skip' y 'limit' deben ser mayores o iguales a 0 y 1 respectivamente."
        )
    return paciente_repository.obtener_pacientes(db, skip=skip, limit=limit)

def eliminar_paciente(db: Session, documento: int):
    # Validar existencia del paciente
    paciente = db.query(Paciente).filter(Paciente.documento == documento).first()
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El paciente con el documento {documento} no fue encontrado. Por favor, verifique el documento."
        )
    paciente_repository.eliminar_paciente(db, documento=documento)
    return paciente

def actualizar_paciente(db: Session, documento: int, paciente_data: PacienteUpdate):
    # Validar existencia del paciente
    paciente = db.query(Paciente).filter(Paciente.documento == documento).first()
    if not paciente:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El paciente con el documento {documento} no fue encontrado. Por favor, verifique el documento."
        )
    paciente_actualizado = paciente_repository.actualizar_paciente(db, paciente, paciente_data)
    if not paciente_actualizado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al actualizar el paciente"
        )
    return paciente_actualizado
