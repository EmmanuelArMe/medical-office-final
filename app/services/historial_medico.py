from fastapi import HTTPException, status
from app.models.paciente import Paciente
from sqlalchemy.orm import Session
from app.repositories import historial_medico as historial_medico_repository
from app.schemas.historial_medico import HistorialMedicoCreate, HistorialMedicoUpdate
from app.models.historial_medico import HistorialMedico

def crear_historial_medico(db: Session, historial: HistorialMedicoCreate):
    # Validar existencia del paciente antes de crear el historial
    paciente_existente = db.query(Paciente).filter(Paciente.id == historial.paciente_id).first()
    if not paciente_existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El paciente con el id {historial.paciente_id} no fue encontrado. Por favor, verifique el id."
        )
    # Crear el historial médico
    nuevo_historial = historial_medico_repository.crear_historial_medico(db, historial)
    if not nuevo_historial:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el historial médico"
        )
    return nuevo_historial

def obtener_historial_medico_por_id(db: Session, id: int):
    # Validar existencia del historial médico
    historial = db.query(HistorialMedico).filter(HistorialMedico.id == id).first()
    if not historial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El historial médico con el id {id} no fue encontrado. Por favor, verifique el id."
        )
    return historial_medico_repository.obtener_historial_medico_por_id(db, id=id)

def obtener_historiales_medicos(db: Session, skip: int, limit: int):
    # Validar existencia de los historiales médicos
    historiales = db.query(HistorialMedico).all()
    if not historiales:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron historiales médicos."
        )
    if skip < 0 or limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los parámetros 'skip' y 'limit' deben ser mayores o iguales a 0 y 1 respectivamente."
        )
    return historial_medico_repository.obtener_historiales_medicos(db, skip=skip, limit=limit)

def eliminar_historial_medico(db: Session, id: int):
    # Validar existencia del historial médico
    historial_medico = obtener_historial_medico_por_id(db, id)
    # Eliminar el historial médico
    historial_medico_repository.eliminar_historial_medico(db, id=id)
    return historial_medico

def actualizar_historial_medico(db: Session, id: int, historial_medico_data: HistorialMedicoUpdate):
    # Validar existencia del historial médico
    historial = historial_medico_repository.obtener_historial_medico_por_id(db, id)
    # Validar existencia del paciente
    paciente_existente = db.query(Paciente).filter(Paciente.id == historial_medico_data.paciente_id).first()
    if not paciente_existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El paciente con el id {historial_medico_data.paciente_id} no fue encontrado."
        )
    historial_actualizado = historial_medico_repository.actualizar_historial_medico(db, id, historial, historial_medico_data.model_dump())
    if not historial_actualizado:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al actualizar el historial médico"
        )
    return historial_actualizado


def obtener_historiales_medicos_por_id_paciente(db: Session, paciente_id: int):
    # Validar existencia del paciente
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El paciente con el id {paciente_id} no fue encontrado. Por favor, verifique el id."
        )
    # Validar los historiales médicos por paciente
    historiales = db.query(HistorialMedico).filter(HistorialMedico.paciente_id == paciente_id).all()
    if not historiales:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron historiales médicos para el paciente con id {paciente_id}."
        )
    return historial_medico_repository.obtener_historiales_medicos_por_id_paciente(db, paciente_id=paciente_id)
