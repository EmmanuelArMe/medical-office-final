from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.db.database import get_db # Corrected import
from app.schemas.receta import RecetaCreate, RecetaResponse, RecetaUpdate
from app.services import receta as service
from app.utils.auth import get_current_user
from app.models.usuario import Usuario # For type hinting current_user

router = APIRouter()

# Removed local get_db definition

@router.post(
        "/recetas",
        response_model=RecetaResponse,
        summary="Crear receta",
        description="Crea una nueva receta en el sistema."
)
def crear_receta(receta: RecetaCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    nueva_receta = service.crear_receta(db, receta)
    return JSONResponse(
        content={"message": "Receta creada correctamente", "response": jsonable_encoder(nueva_receta)},
        status_code=status.HTTP_201_CREATED
    )

@router.get(
        "/recetas/{id}",
        response_model=RecetaResponse,
        summary="Obtener receta por ID",
        description="Obtiene una receta por su ID."
)
def obtener_receta_por_id(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    receta = service.obtener_receta_por_id(db, id)
    return JSONResponse(
        content={"message": "Receta obtenida correctamente", "response": jsonable_encoder(receta)},
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/recetas",
        response_model=list[RecetaResponse],
        summary="Obtener lista de recetas",
        description="Obtiene una lista de recetas paginada."
)
def obtener_recetas(skip: int, limit: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    recetas = service.obtener_recetas(db, skip=skip, limit=limit)
    return JSONResponse(
        content={"message": "Lista de recetas obtenida correctamente", "response": jsonable_encoder(recetas)},
        status_code=status.HTTP_200_OK
    )

@router.delete(
        "/recetas/{id}",
        response_model=RecetaResponse,
        summary="Eliminar receta",
        description="Elimina una receta por su ID."
)
def eliminar_receta(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    receta = service.eliminar_receta(db, id)
    return JSONResponse(
        content={"message": "Receta eliminada correctamente", "response": jsonable_encoder(receta)},
        status_code=status.HTTP_200_OK
    )

@router.put(
        "/recetas/{id}",
        response_model=RecetaResponse,
        summary="Actualizar receta",
        description="Actualiza una receta por su ID."
)
def actualizar_receta(id: int, receta_data: RecetaUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    receta = service.actualizar_receta(db, id, receta_data)
    return JSONResponse(
        content={"message": "Receta actualizada correctamente", "response": jsonable_encoder(receta)},
        status_code=status.HTTP_200_OK
    )
    
@router.get(
        "/recetas/cita/{id}",
        response_model=list[RecetaResponse],
        summary="Obtener recetas por ID de cita",
        description="Obtiene una lista de recetas por el ID de la cita."
)
def obtener_recetas_por_cita(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    recetas = service.obtener_recetas_por_cita(db, id)
    return JSONResponse(
        content={"message": "Lista de recetas obtenida correctamente", "response": jsonable_encoder(recetas)},
        status_code=status.HTTP_200_OK
    )