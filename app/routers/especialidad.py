from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.db.database import get_db # Corrected import
from app.schemas.especialidad import EspecialidadCreate, EspecialidadResponse, EspecialidadUpdate
from app.services import especialidad as service
from app.utils.auth import get_current_user
from app.models.usuario import Usuario # For type hinting current_user

router = APIRouter()

# Removed local get_db definition

@router.post(
        "/especialidades",
        response_model=EspecialidadResponse,
        summary="Crear especialidad",
        description="Crea una nueva especialidad en el sistema."
)
def crear_especialidad(especialidad: EspecialidadCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    nueva_especialidad = service.crear_especialidad(db, especialidad)
    return JSONResponse(
        content={"message": "Especialidad creada correctamente", "response": jsonable_encoder(nueva_especialidad)},
        status_code=status.HTTP_201_CREATED
    )

@router.get(
        "/especialidades/{id}",
        response_model=EspecialidadResponse,
        summary="Obtener especialidad por ID",
        description="Obtiene una especialidad por su ID."
)
def obtener_especialidad_por_id(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    especialidad = service.obtener_especialidad_por_id(db, id)
    return JSONResponse(
        content={"message": "Especialidad obtenida correctamente", "response": jsonable_encoder(especialidad)},
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/especialidades",
        response_model=list[EspecialidadResponse],
        summary="Obtener lista de especialidades",
        description="Obtiene una lista de especialidades paginada."
)
def obtener_especialidades(skip: int, limit: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    especialidades = service.obtener_especialidades(db, skip=skip, limit=limit)
    return JSONResponse(
        content={"message": "Lista de especialidades obtenida correctamente", "response": jsonable_encoder(especialidades)},
        status_code=status.HTTP_200_OK
    )

@router.delete(
        "/especialidades/{id}",
        response_model=EspecialidadResponse,
        summary="Eliminar especialidad",
        description="Elimina una especialidad por su ID."
)
def eliminar_especialidad(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    especialidad_eliminada = service.eliminar_especialidad(db, id)
    return JSONResponse(
        content={"message": f"Especialidad con ID {id} eliminada correctamente", "response": jsonable_encoder(especialidad_eliminada)},
        status_code=status.HTTP_200_OK
    )

@router.put(
        "/especialidades/{id}",
        response_model=EspecialidadResponse,
        summary="Actualizar especialidad",
        description="Actualiza una especialidad por su ID."
)
def actualizar_especialidad(id: int, especialidad: EspecialidadUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    especialidad_actualizada = service.actualizar_especialidad(db, id, especialidad)
    return JSONResponse(
        content={"message": f"Especialidad con ID {id} actualizada correctamente", "response": jsonable_encoder(especialidad_actualizada)},
        status_code=status.HTTP_200_OK
    )