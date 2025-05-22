from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.db.database import get_db # Corrected import
from app.schemas.medico import MedicoCreate, MedicoResponse, MedicoUpdate
from app.services import medico as service
from app.utils.auth import get_current_user
from app.models.usuario import Usuario # For type hinting current_user

router = APIRouter()

# Removed local get_db definition

@router.post(
        "/medicos",
        response_model=MedicoResponse,
        summary="Crear médico",
        description="Crea un nuevo médico en el sistema."
)
def crear_medico(medico: MedicoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    nuevo_medico = service.crear_medico(db, medico)
    return JSONResponse(
        content={
            "message": "Médico creado correctamente",
            "response": jsonable_encoder(nuevo_medico)
        },
        status_code=status.HTTP_201_CREATED
    )
@router.get(
        "/medicos/{documento}",
        response_model=MedicoResponse,
        summary="Obtener médico por documento",
        description="Obtiene un médico por su documento de identidad."
)
def obtener_medico_por_documento(documento: str, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    medico = service.obtener_medico_por_documento(db, documento)
    return JSONResponse(
        content={
            "message": "Médico obtenido correctamente",
            "response": jsonable_encoder(medico)
        },
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/medicos",
        response_model=list[MedicoResponse],
        summary="Obtener lista de médicos",
        description="Obtiene una lista de médicos paginada."
)
def obtener_medicos(skip: int, limit: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return JSONResponse(
        content={
            "message": "Lista de médicos obtenida correctamente",
            "response": jsonable_encoder(service.obtener_medicos(db, skip, limit))
        },
        status_code=status.HTTP_200_OK
    )

@router.delete(
        "/medicos/{documento}",
        response_model=MedicoResponse,
        summary="Eliminar médico",
        description="Elimina un médico por su documento de identidad."
)
def eliminar_medico(documento: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    medico = service.eliminar_medico(db, documento)
    return JSONResponse(
        content={
            "message": "Médico eliminado correctamente",
            "response": jsonable_encoder(medico)
        },
        status_code=status.HTTP_200_OK
    )

@router.put(
        "/medicos/{documento}",
        response_model=MedicoResponse,
        summary="Actualizar médico",
        description="Actualiza un médico por su documento de identidad."
)
def actualizar_medico(documento: str, medico: MedicoUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    medico_actualizado = service.actualizar_medico(db, documento, medico)
    return JSONResponse(
        content={
            "message": "Médico actualizado correctamente",
            "response": jsonable_encoder(medico_actualizado)
        },
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/medicos/especialidad/{id}",
        response_model=list[MedicoResponse],
        summary="Obtener médicos por especialidad",
        description="Obtiene una lista de médicos por su especialidad."
)
def obtener_medicos_por_especialidad(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return JSONResponse(
        content={
            "message": "Lista de médicos por especialidad obtenida correctamente",
            "response": jsonable_encoder(service.obtener_medicos_por_especialidad(db, id))
        },
        status_code=status.HTTP_200_OK
    )
