from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.receta import RecetaCreate, RecetaResponse, RecetaUpdate
from app.services import receta as service
from fastapi.encoders import jsonable_encoder

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
        "/recetas",
        response_model=RecetaResponse,
        summary="Crear receta",
        description="Crea una nueva receta en el sistema."
)
def crear_receta(receta: RecetaCreate, db: Session = Depends(get_db)):
    nueva_receta = service.crear_receta(db, receta)
    return JSONResponse(
        content={"message": "Receta creada correctamente", "response": jsonable_encoder(nueva_receta)},
        status_code=status.HTTP_201_CREATED
    )

@router.get(
        "/recetas/{receta_id}",
        response_model=RecetaResponse,
        summary="Obtener receta por ID",
        description="Obtiene una receta por su ID."
)
def obtener_receta_por_id(receta_id: int, db: Session = Depends(get_db)):
    receta = service.obtener_receta_por_id(db, receta_id)
    return JSONResponse(
        content={"message": "Receta obtenida correctamente", "response": jsonable_encoder(receta)},
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/recetas",
        response_model=list[RecetaResponse],
        summary="Obtener recetas",
        description="Obtiene una lista de recetas paginada."
)
def obtener_recetas(skip: int, limit: int, db: Session = Depends(get_db)):
    recetas = service.obtener_recetas(db, skip=skip, limit=limit)
    return JSONResponse(
        content={"message": "Lista de recetas obtenida correctamente", "response": jsonable_encoder(recetas)},
        status_code=status.HTTP_200_OK
    )

@router.delete(
        "/recetas/{receta_id}",
        response_model=RecetaResponse,
        summary="Eliminar receta",
        description="Elimina una receta por su ID."
)
def eliminar_receta(receta_id: int, db: Session = Depends(get_db)):
    receta = service.eliminar_receta(db, receta_id)
    return JSONResponse(
        content={"message": "Receta eliminada correctamente", "response": jsonable_encoder(receta)},
        status_code=status.HTTP_200_OK
    )

@router.put(
        "/recetas/{receta_id}",
        response_model=RecetaResponse,
        summary="Actualizar receta",
        description="Actualiza una receta por su ID."
)
def actualizar_receta(receta_id: int, receta_data: RecetaUpdate, db: Session = Depends(get_db)):
    receta = service.actualizar_receta(db, receta_id, receta_data)
    return JSONResponse(
        content={"message": "Receta actualizada correctamente", "response": jsonable_encoder(receta)},
        status_code=status.HTTP_200_OK
    )