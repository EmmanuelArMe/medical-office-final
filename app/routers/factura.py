from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.factura import FacturaCreate, FacturaResponse, FacturaUpdate
from app.services import factura as service
from fastapi.encoders import jsonable_encoder

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
        "/facturas",
        response_model=FacturaResponse,
        summary="Crear factura",
        description="Crea una nueva factura en el sistema."
)
def crear_factura(factura: FacturaCreate, db: Session = Depends(get_db)):
    nueva_factura = service.crear_factura(db, factura)
    return JSONResponse(
        content={"message": "Factura creada correctamente", "response": jsonable_encoder(nueva_factura)},
        status_code=status.HTTP_201_CREATED
    )

@router.get(
        "/facturas/{id}",
        response_model=FacturaResponse,
        summary="Obtener factura por ID",
        description="Obtiene una factura por su ID."
)
def obtener_factura_por_id(id: int, db: Session = Depends(get_db)):
    factura = service.obtener_factura_por_id(db, id)
    return JSONResponse(
        content={"message": "Factura obtenida correctamente", "response": jsonable_encoder(factura)},
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/facturas",
        response_model=list[FacturaResponse],
        summary="Obtener lista de facturas",
        description="Obtiene una lista de facturas paginada."
)
def obtener_facturas(skip: int, limit: int, db: Session = Depends(get_db)):
    facturas = service.obtener_facturas(db, skip=skip, limit=limit)
    return JSONResponse(
        content={"message": "Lista de facturas obtenida correctamente", "response": jsonable_encoder(facturas)},
        status_code=status.HTTP_200_OK
    )

@router.delete(
        "/facturas/{id}",
        response_model=FacturaResponse,
        summary="Eliminar factura",
        description="Elimina una factura por su ID."
)
def eliminar_factura(id: int, db: Session = Depends(get_db)):
    factura = service.eliminar_factura(db, id)
    return JSONResponse(
        content={"message": f"Factura con ID {id} eliminada correctamente", "response": jsonable_encoder(factura)},
        status_code=status.HTTP_200_OK
    )

@router.put(
        "/facturas/{id}",
        response_model=FacturaResponse,
        summary="Actualizar factura",
        description="Actualiza una factura por su ID."
)
def actualizar_factura(id: int, factura_data: FacturaUpdate, db: Session = Depends(get_db)):
    factura_actualizada = service.actualizar_factura(db, id, factura_data)
    return JSONResponse(
        content={"message": f"Factura con ID {id} actualizada correctamente", "response": jsonable_encoder(factura_actualizada)},
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/facturas/pago/{id}",
        response_model=FacturaResponse,
        summary="Obtener factura por ID de pago",
        description="Obtiene una factura por su ID de pago."
)
def obtener_factura_por_pago_id(id: int, db: Session = Depends(get_db)):
    factura = service.obtener_factura_por_pago_id(db, id)
    return JSONResponse(
        content={"message": "Factura obtenida correctamente", "response": jsonable_encoder(factura)},
        status_code=status.HTTP_200_OK
    )