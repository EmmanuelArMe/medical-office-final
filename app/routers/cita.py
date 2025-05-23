from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.schemas.cita import CitaCreate, CitaResponse, CitaUpdate
from app.services import cita as service
from app.db.database import get_db # Corrected import
from app.utils.auth import get_current_user
from app.models.usuario import Usuario # For type hinting current_user

router = APIRouter()

# Removed local get_db definition

@router.post(
        "/citas",
        response_model=CitaResponse,
        summary="Crear cita",
        description="Crea una nueva cita en el sistema."
)
def crear_cita(cita: CitaCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    nueva_cita = service.crear_cita(db, cita)
    return JSONResponse(
        content={"message": "Cita creada correctamente", "response": jsonable_encoder(nueva_cita)},
        status_code=status.HTTP_201_CREATED
    )

@router.get(
        "/citas/{id}",
        response_model=CitaResponse,
        summary="Obtener cita por ID",
        description="Obtiene una cita por su ID."
)
def obtener_cita_por_id(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    cita = service.obtener_cita_por_id(db, id)
    return JSONResponse(
        content={"message": "Cita obtenida correctamente", "response": jsonable_encoder(cita)},
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/citas",
        response_model=list[CitaResponse],
        summary="Obtener lista de citas",
        description="Obtiene una lista de citas paginada."
)
def obtener_citas(skip: int, limit: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return JSONResponse( 
        content={"message": "Lista de citas obtenida correctamente", "response": jsonable_encoder(service.obtener_citas(db, skip, limit))},
        status_code=status.HTTP_200_OK
    )

@router.delete(
        "/citas/{id}",
        response_model=CitaResponse,
        summary="Eliminar cita",
        description="Elimina una cita por su ID."
)
def eliminar_cita(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    cita = service.eliminar_cita(db, id)
    return JSONResponse(
        content={"message": f"Cita con ID {id} eliminada correctamente", "response": jsonable_encoder(cita)},
        status_code=status.HTTP_200_OK
    )


@router.put(
        "/citas/{id}",
        response_model=CitaResponse,
        summary="Actualizar cita",
        description="Actualiza una cita por su ID."
)
def actualizar_cita(id: int, cita: CitaUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    cita_actualizada = service.actualizar_cita(db, id, cita)
    return JSONResponse(
        content={
            "message": f"Cita con ID {id} actualizada correctamente",
            "response": jsonable_encoder(cita_actualizada)
        },
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/citas/paciente/{id}",
        response_model=list[CitaResponse],
        summary="Obtener citas por paciente",
        description="Obtiene una lista de citas por el ID del paciente."
)
def obtener_citas_por_paciente(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    citas_por_paciente = service.obtener_citas_por_paciente(db, id)
    return JSONResponse(
        content={
            "message": f"Citas obtenidas correctamente para el paciente con ID {id}",
            "response": jsonable_encoder(citas_por_paciente)
        },
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/citas/medico/{id}",
        response_model=list[CitaResponse],
        summary="Obtener citas por médico",
        description="Obtiene una lista de citas por el ID del médico."
)
def obtener_citas_por_medico(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    citas_por_medico = service.obtener_citas_por_medico(db, id)
    return JSONResponse(
        content={
            "message": f"Citas obtenidas correctamente para el médico con ID {id}",
            "response": jsonable_encoder(citas_por_medico)
        },
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/citas/consultorio/{id}",
        response_model=list[CitaResponse],
        summary="Obtener citas por consultorio",
        description="Obtiene una lista de citas por el ID del consultorio."
)
def obtener_citas_por_consultorio(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    citas_por_consultorio = service.obtener_citas_por_consultorio(db, id)
    return JSONResponse(
        content={
            "message": f"Citas obtenidas correctamente para el consultorio con ID {id}",
            "response": jsonable_encoder(citas_por_consultorio)
        },
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/citas/fecha/{fecha}",
        response_model=list[CitaResponse],
        summary="Obtener citas por fecha",
        description="Obtiene una lista de citas por la fecha."
)
def obtener_citas_por_fecha(fecha: str, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    citas_por_fecha = service.obtener_citas_por_fecha(db, fecha)
    return JSONResponse(
        content={
            "message": f"Citas obtenidas correctamente para la fecha {fecha}",
            "response": jsonable_encoder(citas_por_fecha)
        },
        status_code=status.HTTP_200_OK
    )