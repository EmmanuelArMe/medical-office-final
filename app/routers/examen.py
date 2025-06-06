from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.db.database import get_db # Corrected import
from app.schemas.examen import ExamenCreate, ExamenResponse, ExamenUpdate
from app.services import examen as service
from app.utils.auth import get_current_user
from app.models.usuario import Usuario # For type hinting current_user

router = APIRouter()

# Removed local get_db definition

@router.post(
        "/examenes",
        response_model=ExamenResponse,
        summary="Crear examen",
        description="Crea un nuevo examen en el sistema."
)
def crear_examen(examen: ExamenCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    nuevo_examen = service.crear_examen(db, examen)
    return JSONResponse(
        content={"message": "Examen creado correctamente", "response": jsonable_encoder(nuevo_examen)},
        status_code=status.HTTP_201_CREATED
    )

@router.get(
        "/examenes/{id}",
        response_model=ExamenResponse,
        summary="Obtener examen por ID",
        description="Obtiene un examen por su ID."
)
def obtener_examen_por_id(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    examen = service.obtener_examen_por_id(db, id)
    return JSONResponse(
        content={"message": "Examen obtenido correctamente", "response": jsonable_encoder(examen)},
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/examenes",
        response_model=list[ExamenResponse],
        summary="Obtener lista de examenes",
        description="Obtiene una lista de examenes paginada."
)
def obtener_examenes(skip: int, limit: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    examenes = service.obtener_examenes(db, skip=skip, limit=limit)
    return JSONResponse(
        content={"message": "Lista de examenes obtenida correctamente", "response": jsonable_encoder(examenes)},
        status_code=status.HTTP_200_OK
    )

@router.delete(
        "/examenes/{id}",
        response_model=ExamenResponse,
        summary="Eliminar examen",
        description="Elimina un examen por su ID."
)
def eliminar_examen(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    examen = service.eliminar_examen(db, id)
    return JSONResponse(
        content={"message": f"Examen con ID {id} eliminado correctamente", "response": jsonable_encoder(examen)},
        status_code=status.HTTP_200_OK
    )

@router.put(
        "/examenes/{id}",
        response_model=ExamenResponse,
        summary="Actualizar examen",
        description="Actualiza un examen por su ID."
)
def actualizar_examen(id: int, examen: ExamenUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    examen_actualizado = service.actualizar_examen(db, id, examen)
    return JSONResponse(
        content={"message": f"Examen con ID {id} actualizado correctamente", "response": jsonable_encoder(examen_actualizado)},
        status_code=status.HTTP_200_OK
    )