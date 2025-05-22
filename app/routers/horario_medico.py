from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.db.database import get_db # Corrected import
from app.schemas.horario_medico import HorarioMedicoCreate, HorarioMedicoResponse, HorarioMedicoUpdate
from app.services import horario_medico as service
from app.utils.auth import get_current_user
from app.models.usuario import Usuario # For type hinting current_user

router = APIRouter()

# Removed local get_db definition

@router.post(
        "/horarios",
        response_model=HorarioMedicoResponse,
        summary="Crear horario médico",
        description="Crea un nuevo horario médico en el sistema."
)
def crear_horario_medico(horario: HorarioMedicoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    nuevo_horario_medico = service.crear_horario_medico(db, horario)
    return JSONResponse(
        content={
            "message": "Horario médico creado correctamente",
            "response": jsonable_encoder(nuevo_horario_medico)
        }, 
        status_code=status.HTTP_201_CREATED
    )

@router.get(
        "/horario/{id}",
        response_model=HorarioMedicoResponse,
        summary="Obtener horario médico por ID",
        description="Obtiene un horario médico por su ID."
)
def obtener_horario_medico_por_id(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    horario_medico = service.obtener_horario_medico_por_id(db, id)
    return JSONResponse(
        content={
            "message": f"Horario médico con el {id}, obtenido correctamente",
            "response": jsonable_encoder(horario_medico)
        },
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/horarios",
        response_model=list[HorarioMedicoResponse],
        summary="Obtener lista de horarios médicos",
        description="Obtiene una lista de horarios médicos paginada.")
def obtener_horarios_medicos(skip: int, limit: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return JSONResponse(
        content={
            "message": "Lista de horarios médicos obtenidos correctamente",
            "response": jsonable_encoder(service.obtener_horarios_medicos(db, skip, limit))
        },
        status_code=status.HTTP_200_OK)

@router.delete(
        "/horario/{id}",
        response_model=HorarioMedicoResponse,
        summary="Eliminar horario médico",
        description="Elimina un horario médico por su ID.")
def eliminar_horario_medico(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    horario_medico = service.eliminar_horario_medico(db, id)
    return JSONResponse(
        content={
            "message": f"Horario médico con el id {id}, eliminado correctamente",
            "response": jsonable_encoder(horario_medico)
        }, 
        status_code=status.HTTP_200_OK
    )

@router.put(
        "/horarios/{id}",
        response_model=HorarioMedicoResponse,
        summary="Actualizar horario médico",
        description="Actualiza un horario médico por su ID.")
def actualizar_horario_medico(id: int, horario: HorarioMedicoUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    Horario_medico_actualizado = service.actualizar_horario_medico(db, id, horario)
    return JSONResponse(
        content={
            "message": f"Horario médico con el id {id} ha sido actualizado correctamente",
            "response": jsonable_encoder(Horario_medico_actualizado)
        },
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/horarios/medico/{id}",
        response_model=list[HorarioMedicoResponse],
        summary="Obtener horarios médicos por ID de médico",
        description="Obtiene una lista de horarios médicos por el ID del médico.")
def obtener_horarios_medicos_por_medico_id(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    horarios_medicos = service.obtener_horarios_medicos_por_id_medico(db, id)
    return JSONResponse(
        content={
            "message": f"Lista de horarios médicos del médico con ID {id} obtenidos correctamente",
            "response": jsonable_encoder(horarios_medicos)
        },
        status_code=status.HTTP_200_OK
    )