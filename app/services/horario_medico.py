from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.horario_medico import HorarioMedicoCreate, HorarioMedicoUpdate
from app.models.horario_medico import HorarioMedico
from app.repositories import horario_medico as horario_repository
from app.models.medico import Medico

def crear_horario_medico(db: Session, horario_medico: HorarioMedicoCreate):
    # validar la existencia del medico
    medico = db.query(HorarioMedico).filter(HorarioMedico.id == horario_medico.medico_id).first()
    if not medico:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El médico con ID {horario_medico.medico_id} no fue encontrado. Por favor, verifique el ID."
        )
    nuevo_horario = horario_repository.crear_horario_medico(db, horario_medico)
    if not nuevo_horario:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el horario médico"
        )
    return nuevo_horario

def obtener_horario_medico_por_id(db: Session, id: int):
    # Validar existencia del horario médico
    horario_medico = db.query(HorarioMedico).filter(HorarioMedico.id == id).first()
    if not horario_medico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El horario médico con ID {id} no fue encontrado. Por favor, verifique el ID."
        )
    return horario_repository.obtener_horario_medico_por_id(db, id=id)

def obtener_horarios_medicos(db: Session, skip: int, limit: int):
    # Validar existencia de los horarios médicos
    horarios_medicos = db.query(HorarioMedico).all()
    if not horarios_medicos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron horarios médicos."
        )
    if skip < 0 or limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los parámetros 'skip' y 'limit' deben ser mayores o iguales a 0 y 1 respectivamente."
        )
    return horario_repository.obtener_horarios_medicos(db, skip=skip, limit=limit)

def eliminar_horario_medico(db: Session, id: int):
    # Validar existencia del horario médico
    horario_medico = obtener_horario_medico_por_id(db, id)
    horario_repository.eliminar_horario_medico(db, id=id)
    return horario_medico

def actualizar_horario_medico(db: Session, id: int, horario_medico_data: HorarioMedicoUpdate):
    # Validar existencia del horario médico
    horario_medico = obtener_horario_medico_por_id(db, id)
    # Validar la existencia del médico
    medico = db.query(HorarioMedico).filter(HorarioMedico.id == horario_medico_data.medico_id).first()
    if not medico:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El médico con ID {horario_medico_data.medico_id} no fue encontrado. Por favor, verifique el ID."
        )
    horario_actualizado = horario_repository.actualizar_horario_medico(db, horario_medico, horario_medico_data)
    if not horario_actualizado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al actualizar el horario médico"
        )
    return horario_actualizado

def obtener_horarios_medicos_por_id_medico(db: Session, medico_id: int):
    # Validar existencia del médico
    medico = db.query(Medico).filter(Medico.id == medico_id).first()
    if not medico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un médico con id {medico_id}"
        )
    horarios_medicos = horario_repository.obtener_horarios_medicos_por_id_medico(db, medico_id=medico_id)
    if not horarios_medicos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron horarios médicos para el médico con ID {medico_id}."
        )
    return horarios_medicos
