from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import resultado_examen as resultado_examen_repository
from app.models.resultado_examen import ResultadoExamen
from app.models.paciente import Paciente
from app.models.examen import Examen
from app.schemas.resultado_examen import ResultadoExamenCreate, ResultadoExamenUpdate

def crear_resultado_examen(db: Session, resultado_examen: ResultadoExamenCreate):
    # Validar existencia del paciente
    paciente = db.query(Paciente).filter(Paciente.id == resultado_examen.paciente_id).first()
    if not paciente:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El paciente con ID {resultado_examen.paciente_id} no existe"
        )
    # Validar existencia del examen
    examen = db.query(Examen).filter(Examen.id == resultado_examen.examen_id).first()
    if not examen:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El examen con ID {resultado_examen.examen_id} no existe"
        )
    nuevo_resultado_examen = resultado_examen_repository.crear_resultado_examen(db, resultado_examen)
    if not nuevo_resultado_examen:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el resultado_examen"
        )
    return nuevo_resultado_examen

def obtener_resultado_examen_por_id(db: Session, resultado_examen_id: int):
    # Validar existencia del resultado_examen
    resultado_examen = db.query(ResultadoExamen).filter(ResultadoExamen.id == resultado_examen_id).first()
    if not resultado_examen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El resultado_examen con el id {resultado_examen_id} no fue encontrado. Por favor, verifique el id."
        )
    return resultado_examen_repository.obtener_resultado_examen_por_id(db, resultado_examen_id)
    
def obtener_resultados_examenes(db: Session, skip: int, limit: int):
    # Validar existencia de los resultados_examenes
    resultados_examenes = db.query(ResultadoExamen).all()
    if not resultados_examenes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron resultados_examenes."
        )
    if skip < 0 or limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los parámetros 'skip' y 'limit' deben ser mayores o iguales a 0 y 1 respectivamente."
        )
    return resultado_examen_repository.obtener_resultados_examenes(db, skip=skip, limit=limit)

def eliminar_resultado_examen(db: Session, resultado_examen_id: int):
    # Validar existencia del resultado_examen
    resultado_examen = obtener_resultado_examen_por_id(db, resultado_examen_id)
    resultado_examen_repository.eliminar_resultado_examen(db, resultado_examen_id)
    return resultado_examen

def actualizar_resultado_examen(db: Session, resultado_examen_id: int, resultado_examen_data: ResultadoExamenUpdate):
    # Validar existencia del resultado_examen
    resultado_examen = obtener_resultado_examen_por_id(db, resultado_examen_id)
    # Validar existencia del paciente
    paciente = db.query(Paciente).filter(Paciente.id == resultado_examen_data.paciente_id).first()
    if not paciente:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El paciente con ID {resultado_examen_data.paciente_id} no existe"
        )
    # Validar existencia del examen
    examen = db.query(Examen).filter(Examen.id == resultado_examen_data.examen_id).first()
    if not examen:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El examen con ID {resultado_examen_data.examen_id} no existe"
        )
    resultado_examen_actualizada = resultado_examen_repository.actualizar_resultado_examen(db, resultado_examen, resultado_examen_data)
    if not resultado_examen_actualizada:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al actualizar el resultado_examen"
        )
    return resultado_examen_actualizada

def obtener_resultados_examenes_por_paciente(db: Session, paciente_id: int):
    # Validar existencia del paciente
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron resultados de examenes para el paciente con ID {paciente_id}."
        )
    return resultado_examen_repository.obtener_resultados_examenes_por_paciente(db, paciente_id)

def obtener_resultados_examenes_por_examen(db: Session, examen_id: int):
    # Validar existencia del examen
    examen = db.query(Examen).filter(Examen.id == examen_id).first()
    if not examen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron resultados de examenes para el examen con ID {examen_id}."
        )
    return resultado_examen_repository.obtener_resultados_examenes_por_examen(db, examen_id)
