from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import resultado_examen as resultado_examen_repository
from app.models.resultado_examen import ResultadoExamen
from app.schemas.resultado_examen import ResultadoExamenCreate, ResultadoExamenUpdate

def crear_resultado_examen(db: Session, resultado_examen: ResultadoExamenCreate):
    # Validar existencia del resultado_examen
    resultado_examen_existente = db.query(ResultadoExamen).filter(ResultadoExamen.id == resultado_examen.id).first()
    if resultado_examen_existente:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un resultado_examen con el id {resultado_examen.id}"
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
    return resultado_examen_repository.obtener_resultado_examen(db, skip=skip, limit=limit)

def eliminar_resultado_examen(db: Session, resultado_examen_id: int):
    # Validar existencia del resultado_examen
    resultado_examen = obtener_resultado_examen_por_id(db, resultado_examen_id)
    resultado_examen_repository.eliminar_resultado_examen(db, resultado_examen_id)
    return resultado_examen

def actualizar_resultado_examen(db: Session, resultado_examen_id: int, resultado_examen_data: ResultadoExamenUpdate):
    # Validar existencia del resultado_examen
    resultado_examen = obtener_resultado_examen_por_id(db, resultado_examen_id)
    resultado_examen_actualizada = resultado_examen_repository.actualizar_resultado_examen(db, resultado_examen, resultado_examen_data)
    if not resultado_examen_actualizada:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al actualizar el resultado_examen"
        )
    return resultado_examen_actualizada
