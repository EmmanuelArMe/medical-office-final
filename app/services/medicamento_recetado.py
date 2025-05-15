from fastapi import HTTPException, status
from app.models import MedicamentoRecetado, Receta, Medicamento
from app.schemas.medicamento_recetado import MedicamentoRecetadoCreate, MedicamentoRecetadoUpdate
from sqlalchemy.orm import Session
from app.repositories import medicamento_recetado as medicamento_recetado_repository

def crear_medicamento_recetado(db: Session, medicamento_recetado_data: MedicamentoRecetadoCreate):
    # Validar existencia de la cita
    receta = db.query(Receta).filter(Receta.id == medicamento_recetado_data.receta_id).first()
    if not receta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una receta con id {medicamento_recetado_data.receta_id}"
        )

    # Validar existencia del medicamento
    medicamento = db.query(Medicamento).filter(Medicamento.id == medicamento_recetado_data.medicamento_id).first()
    if not medicamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un medicamento con id {medicamento_recetado_data.medicamento_id}"
        )

    # Crear el medicamento recetado
    nuevo_medicamento_recetado = medicamento_recetado_repository.crear_medicamento_recetado(db, medicamento_recetado_data)
    if not nuevo_medicamento_recetado:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el medicamento recetado"
        )
    return nuevo_medicamento_recetado

def obtener_medicamento_recetado_por_id(db: Session, medicamento_recetado_id: int):
    # Validar existencia del medicamento recetado
    medicamento_recetado = db.query(MedicamentoRecetado).filter(MedicamentoRecetado.id == medicamento_recetado_id).first()
    if not medicamento_recetado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un medicamento recetado con id {medicamento_recetado_id}"
        )
    return medicamento_recetado

def obtener_medicamentos_recetados(db: Session, skip: int = 0, limit: int = 100):
    # Obtener todos los medicamentos recetados
    medicamentos_recetados = medicamento_recetado_repository.obtener_medicamentos_recetados(db, skip, limit)
    if not medicamentos_recetados:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron medicamentos recetados"
        )
    if skip < 0 or limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los parámetros 'skip' y 'limit' deben ser mayores o iguales a 0 y 1 respectivamente."
        )
    return medicamentos_recetados

def eliminar_medicamento_recetado(db: Session, medicamento_recetado_id: int):
    # Validar existencia del medicamento recetado
    medicamento_recetado = obtener_medicamento_recetado_por_id(db, medicamento_recetado_id)
    # Eliminar el medicamento recetado
    medicamento_recetado_repository.eliminar_medicamento_recetado(db, medicamento_recetado_id)
    return medicamento_recetado

def actualizar_medicamento_recetado(db: Session, medicamento_recetado_id: int, medicamento_recetado_data: MedicamentoRecetadoUpdate):
    # Validar existencia del medicamento recetado
    medicamento_recetado = obtener_medicamento_recetado_por_id(db, medicamento_recetado_id)
    # Validar existencia de la cita
    cita = db.query(Receta).filter(Receta.id == medicamento_recetado_data.receta_id).first()
    if not cita:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una cita con id {medicamento_recetado_data.receta_id}"
        )

    # Validar existencia del medicamento
    medicamento = db.query(Medicamento).filter(Medicamento.id == medicamento_recetado_data.medicamento_id).first()
    if not medicamento:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un medicamento con id {medicamento_recetado_data.medicamento_id}"
        )

    # Actualizar el medicamento recetado
    actualizado_medicamento_recetado = medicamento_recetado_repository.actualizar_medicamento_recetado(db, medicamento_recetado, medicamento_recetado_data)
    if not actualizado_medicamento_recetado:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al actualizar el medicamento recetado"
        )
    return actualizado_medicamento_recetado

def obtener_medicamentos_recetados_por_receta(db: Session, receta_id: int):
    # Validar existencia de la receta
    receta = db.query(Receta).filter(Receta.id == receta_id).first()
    if not receta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una receta con id {receta_id}"
        )
    # Obtener medicamentos recetados por receta
    medicamentos_recetados = medicamento_recetado_repository.obtener_medicamentos_recetados_por_receta(db, receta_id)
    if not medicamentos_recetados:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron medicamentos recetados para la receta con id {receta_id}"
        )
    return medicamentos_recetados

def obtener_medicamentos_recetados_por_medicamento(db: Session, medicamento_id: int):
    # Validar existencia del medicamento
    medicamento = db.query(Medicamento).filter(Medicamento.id == medicamento_id).first()
    if not medicamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró un medicamento con id {medicamento_id}"
        )
    # Obtener medicamentos recetados por medicamento
    medicamentos_recetados = medicamento_recetado_repository.obtener_medicamentos_recetados_por_medicamento(db, medicamento_id)
    if not medicamentos_recetados:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron medicamentos recetados para el medicamento con id {medicamento_id}"
        )
    return medicamentos_recetados