from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import factura as factura_repository
from app.models.factura import Factura
from app.schemas.factura import FacturaCreate, FacturaUpdate
from app.models.pago import Pago

def crear_factura(db: Session, factura_data: FacturaCreate):
    # Validar existencia del pago
    pago = db.query(Pago).filter(Pago.id == factura_data.pago_id).first()
    if not pago:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El pago con el id {factura_data.pago_id} no fue encontrado."
        )
    nueva_factura = factura_repository.crear_factura(db, factura_data)
    if not nueva_factura:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear la factura"
        )
    return nueva_factura

def obtener_factura_por_id(db: Session, factura_id: int):
    # Validar existencia de la factura
    factura = db.query(Factura).filter(Factura.id == factura_id).first()
    if not factura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La factura con el id {factura_id} no fue encontrada. Por favor, verifique el id."
        )
    return factura_repository.obtener_factura_por_id(db, factura_id)

def obtener_facturas(db: Session, skip: int, limit: int):
    # Validar existencia de la factura
    facturas = db.query(Factura).all()
    if not facturas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron facturas."
        )
    if skip < 0 or limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los parámetros 'skip' y 'limit' deben ser mayores o iguales a 0 y 1 respectivamente."
        )
    return factura_repository.obtener_facturas(db, skip=skip, limit=limit)

def eliminar_factura(db: Session, factura_id: int):
    # Validar existencia de la factura
    factura = obtener_factura_por_id(db, factura_id)
    factura_repository.eliminar_factura(db, factura_id)
    return factura

def actualizar_factura(db: Session, factura_id: int, factura_data: FacturaUpdate):
    # Validar existencia de la factura
    factura = obtener_factura_por_id(db, factura_id)
    # Validar existencia del pago
    pago = db.query(Pago).filter(Pago.id == factura_data.pago_id).first()
    if not pago:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El pago con el id {factura_data.pago_id} no fue encontrado."
        )
    # Actualizar la factura
    factura_actualizada = factura_repository.actualizar_factura(db, factura, factura_data)
    if not factura:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al actualizar la factura"
        )
    return factura_actualizada

def obtener_factura_por_pago_id(db: Session, pago_id: int):
    # Validar existencia de la factura
    factura = db.query(Factura).filter(Factura.pago_id == pago_id).first()
    if not factura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron facturas para el pago con el id {pago_id}. Por favor, verifique el id."
        )
    return factura_repository.obtener_factura_por_pago_id(db, pago_id)