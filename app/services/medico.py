from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.medico import MedicoCreate, MedicoUpdate
from app.models.medico import Medico
from app.models.especialidad import Especialidad
from app.repositories import medico as medico_repository

def crear_medico(db: Session, medico_data: MedicoCreate) -> Medico:
    # Validar existencia del médico
    medico_existente = db.query(Medico).filter(Medico.documento == medico_data.documento).first()
    if medico_existente:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un médico con el documento {medico_data.documento}"
        )
    # Validar existencia de la especialidad
    especialidad = db.query(Especialidad).filter(Especialidad.id == medico_data.especialidad_id).first()
    if not especialidad:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La especialidad con ID {medico_data.especialidad_id} no existe"
        )
    nuevo_medico = medico_repository.crear_medico(db, medico_data)
    if not nuevo_medico:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el médico"
        )
    return nuevo_medico

def obtener_medico_por_documento(db: Session, medico_documento: int) -> Medico:
    # Validar existencia del médico
    medico = db.query(Medico).filter(Medico.documento == medico_documento).first()
    if not medico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El médico con documento {medico_documento} no fue encontrado. Por favor, verifique el documento."
        )
    return medico_repository.obtener_medico_por_documento(db, medico_documento)

def obtener_medicos(db: Session, skip: int, limit: int) -> list[Medico]:
    # Validar existencia de los médicos
    medicos = db.query(Medico).all()
    if not medicos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron médicos."
        )
    if skip < 0 or limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los parámetros 'skip' y 'limit' deben ser mayores o iguales a 0 y 1 respectivamente."
        )
    return medico_repository.obtener_medicos(db, skip=skip, limit=limit)

def eliminar_medico(db: Session, medico_documento: int) -> Medico:
    # Validar existencia del médico
    medico = db.query(Medico).filter(Medico.documento == medico_documento).first()
    if not medico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El médico con documento {medico_documento} no fue encontrado. Por favor, verifique el documento."
        )
    medico_repository.eliminar_medico(db, medico_documento=medico_documento)
    return medico

def actualizar_medico(db: Session, medico_documento: int, medico_data: MedicoUpdate) -> Medico:
    # Validar existencia del médico
    medico = db.query(Medico).filter(Medico.documento == medico_documento).first()
    if not medico:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El médico con documento {medico_documento} no fue encontrado. Por favor, verifique el documento."
        )
    # Validar existencia de la especialidad
    especialidad = db.query(Especialidad).filter(Especialidad.id == medico_data.especialidad_id).first()
    if not especialidad:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La especialidad con ID {medico_data.especialidad_id} no existe"
        )
    medico_actualizado = medico_repository.actualizar_medico(db, medico, medico_data)
    if not medico_actualizado:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al actualizar el médico"
        )
    return medico_actualizado

def obtener_medicos_por_especialidad(db: Session, especialidad_id: int) -> list[Medico]:
    # Validar existencia de la especialidad
    especialidad = db.query(Especialidad).filter(Especialidad.id == especialidad_id).first()
    if not especialidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La especialidad con ID {especialidad_id} no fue encontrada. Por favor, verifique el ID."
        )
    # Validar existencia de los médicos
    medicos = db.query(Medico).filter(Medico.especialidad_id == especialidad_id).all()
    if not medicos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron médicos para la especialidad seleccionada."
        )
    return medico_repository.obtener_medicos_por_especialidad(db, especialidad_id)