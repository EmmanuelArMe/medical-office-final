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

def obtener_paciente_por_documento(db: Session, documento: str):
    # Validar existencia del paciente
    paciente = paciente_repository.obtener_paciente_por_documento(db, documento=documento)
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El paciente con el documento {documento} no fue encontrado. Por favor, verifique el documento."
        )
    try:
        return {
            "id": paciente.id,
            "nombre": paciente.nombre,
            "apellido": paciente.apellido,
            "fecha_nacimiento": paciente.fecha_nacimiento,
            "documento": paciente.documento,
            "telefono": paciente.telefono,  # desencriptado
            "email": paciente.email,        # desencriptado
        }
    except Exception:
        return {
            "id": paciente.id,
            "nombre": paciente.nombre,
            "apellido": paciente.apellido,
            "fecha_nacimiento": paciente.fecha_nacimiento,
            "documento": paciente.documento,
            "telefono": "[ERROR DE ENCRIPTACIÓN]" if paciente._telefono else None,
            "email": "[ERROR DE ENCRIPTACIÓN]" if paciente._email else None,
        }

    
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

def eliminar_paciente(db: Session, documento: str):
    # Validar existencia del paciente
    paciente = obtener_paciente_por_documento(db, documento=documento)
    paciente_repository.eliminar_paciente(db, documento=documento)
    return paciente

def actualizar_paciente(db: Session, documento: str, paciente_data: PacienteUpdate):
    # Validar existencia del paciente
    paciente = paciente_repository.obtener_paciente_por_documento(db, documento=documento)
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El paciente con el documento {documento} no fue encontrado. Por favor, verifique el documento."
        )
    # Validar existencia del paciente con el mismo documento
    paciente_existente = db.query(Paciente).filter(Paciente.documento == paciente_data.documento).first()
    if paciente_existente:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un paciente con el documento {paciente_data.documento}"
        )
    paciente_actualizado = paciente_repository.actualizar_paciente(db, paciente, paciente_data)
    if not paciente_actualizado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al actualizar el paciente"
        )
        
    try:
        return {
            "id": paciente_actualizado.id,
            "nombre": paciente_actualizado.nombre,
            "apellido": paciente_actualizado.apellido,
            "fecha_nacimiento": paciente_actualizado.fecha_nacimiento,
            "documento": paciente_actualizado.documento,
            "telefono": paciente_actualizado.telefono,  # desencriptado
            "email": paciente_actualizado.email,        # desencriptado
        }
    except Exception:
        return {
            "id": paciente_actualizado.id,
            "nombre": paciente_actualizado.nombre,
            "apellido": paciente_actualizado.apellido,
            "fecha_nacimiento": paciente_actualizado.fecha_nacimiento,
            "documento": paciente_actualizado.documento,
            "telefono": "[ERROR DE ENCRIPTACIÓN]" if paciente_actualizado._telefono else None,
            "email": "[ERROR DE ENCRIPTACIÓN]" if paciente_actualizado._email else None,
        }
