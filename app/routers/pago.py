from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.pago import PagoCreate, PagoResponse, PagoUpdate
from app.services import pago as service
from fastapi.encoders import jsonable_encoder

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
        "/pagos",
        response_model=PagoResponse,
        summary="Crear pago",
        description="Crea un nuevo pago en el sistema."
)
def crear_pago(pago: PagoCreate, db: Session = Depends(get_db)):
    nuevo_pago = service.crear_pago(db, pago)
    return JSONResponse(
        content={"message": "Pago creado correctamente", "response": jsonable_encoder(nuevo_pago)},
        status_code=status.HTTP_201_CREATED
    )

@router.get(
        "/pagos/{pago_id}",
        response_model=PagoResponse,
        summary="Obtener pago por ID",
        description="Obtiene un pago por su ID."
)
def obtener_pago_por_id(pago_id: int, db: Session = Depends(get_db)):
    pago = service.obtener_pago_por_id(db, pago_id)
    return JSONResponse(
        content={"message": "Pago obtenido correctamente", "response": jsonable_encoder(pago)},
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/pagos",
        response_model=list[PagoResponse],
        summary="Obtener pagos",
        description="Obtiene una lista de pagos paginada."
)
def obtener_pagos(skip: int, limit: int, db: Session = Depends(get_db)):
    pagos = service.obtener_pagos(db, skip=skip, limit=limit)
    return JSONResponse(
        content={"message": "Lista de pagos obtenida correctamente", "response": jsonable_encoder(pagos)},
        status_code=status.HTTP_200_OK
    )

@router.delete(
        "/pagos/{pago_id}",
        response_model=PagoResponse,
        summary="Eliminar pago",
        description="Elimina un pago por su ID."
)
def eliminar_pago(pago_id: int, db: Session = Depends(get_db)):
    pago = service.eliminar_pago(db, pago_id)
    return JSONResponse(
        content={"message": "Pago eliminado correctamente", "response": jsonable_encoder(pago)},
        status_code=status.HTTP_200_OK
    )

@router.put(
        "/pagos/{pago_id}",
        response_model=PagoResponse,
        summary="Actualizar pago",
        description="Actualiza un pago por su ID."
)
def actualizar_pago(pago_id: int, pago_data: PagoUpdate, db: Session = Depends(get_db)):
    pago = service.actualizar_pago(db, pago_id, pago_data)
    return JSONResponse(
        content={"message": "Pago actualizado correctamente", "response": jsonable_encoder(pago)},
        status_code=status.HTTP_200_OK
    )