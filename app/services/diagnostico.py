from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.diagnostico import DiagnosticoCreate, DiagnosticoUpdate
from app.models.cita import Cita
from app.models.diagnostico import Diagnostico
from app.repositories import diagnostico as diagnostico_repository

def crear_diagnostico(db: Session, diagnostico_data: DiagnosticoCreate):
    # Validar existencia de la cita
    cita = db.query(Cita).filter(Cita.id == diagnostico_data.cita_id).first()
    if not cita:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una cita con id {diagnostico_data.cita_id}"
        )
    diagnostico_nuevo = diagnostico_repository.crear_diagnostico(db, diagnostico_data)
    if not diagnostico_nuevo:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el diagnóstico"
        )
    return diagnostico_nuevo

def obtener_diagnostico_por_id(db: Session, diagnostico_id: int):
    # Validar existencia del diagnóstico
    diagnostico = db.query(Diagnostico).filter(Diagnostico.id == diagnostico_id).first()
    if not diagnostico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un diagnóstico con id {diagnostico_id}"
        )
    return diagnostico_repository.obtener_diagnostico_por_id(db, diagnostico_id)

def obtener_diagnosticos(db: Session, skip: int, limit: int):
    # Validar existencia de los diagnósticos
    diagnosticos = db.query(Diagnostico).all()
    if not diagnosticos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron diagnósticos."
        )
    if skip < 0 or limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los parámetros 'skip' y 'limit' deben ser mayores o iguales a 0 y 1 respectivamente."
        )
    return diagnostico_repository.obtener_diagnosticos(db, skip = skip, limit = limit)

def eliminar_diagnostico(db: Session, diagnostico_id: int):
    # Validar existencia del diagnóstico
    diagnostico = db.query(Diagnostico).filter(Diagnostico.id == diagnostico_id).first()
    if not diagnostico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un diagnóstico con id {diagnostico_id}, por favor, verifique el id."
        )
    diagnostico_repository.eliminar_diagnostico(db, diagnostico_id)
    return diagnostico

def actualizar_diagnostico(db: Session, diagnostico_id: int, diagnostico_data: DiagnosticoUpdate):
    # Validar existencia del diagnóstico
    diagnostico = db.query(Diagnostico).filter(Diagnostico.id == diagnostico_id).first()
    if not diagnostico:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un diagnóstico con id {diagnostico_id}, por favor, verifique el id."
        )
    # Validar existencia de la cita
    cita = db.query(Cita).filter(Cita.id == diagnostico_data.cita_id).first()
    if not cita:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una cita con id {diagnostico_data.cita_id}"
        )
    # Actualizar el diagnóstico
    diagnostico_actualizado = diagnostico_repository.actualizar_diagnostico(db, diagnostico, diagnostico_data)
    if not diagnostico_actualizado:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al actualizar el diagnóstico"
        )
    return diagnostico_actualizado

def obtener_diagnosticos_por_cita(db: Session, cita_id: int):
    # Validar existencia de la cita
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una cita con id {cita_id}"
        )
    
    # Validar existencia del diagnóstico asociado a la cita
    diagnosticos = db.query(Diagnostico).filter(Diagnostico.cita_id == cita_id).all()
    if not diagnosticos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron diagnósticos asociados a la cita con id {cita_id}"
        )
    return diagnostico_repository.obtener_diagnosticos_por_cita(db, cita_id)