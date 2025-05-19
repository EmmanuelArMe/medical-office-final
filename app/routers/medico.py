from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.medico import MedicoCreate, MedicoResponse, MedicoUpdate
from app.services import medico as service
from fastapi.encoders import jsonable_encoder

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
        "/medicos",
        response_model=MedicoResponse,
        summary="Crear médico",
        description="Crea un nuevo médico en el sistema."
)
def crear_medico(medico: MedicoCreate, db: Session = Depends(get_db)):
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
def obtener_medico_por_documento(documento: str, db: Session = Depends(get_db)):
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
def obtener_medicos(skip: int, limit: int, db: Session = Depends(get_db)):
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
def eliminar_medico(documento: int, db: Session = Depends(get_db)):
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
def actualizar_medico(documento: str, medico: MedicoUpdate, db: Session = Depends(get_db)):
    medico_actualizado = service.actualizar_medico(db, documento, medico)
    return JSONResponse(
        content={
            "message": "Médico actualizado correctamente",
            "response": jsonable_encoder(medico_actualizado)
        },
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/medicos/especialidad/{especialidad_id}",
        response_model=list[MedicoResponse],
        summary="Obtener médicos por especialidad",
        description="Obtiene una lista de médicos por su especialidad."
)
def obtener_medicos_por_especialidad(especialidad_id: int, db: Session = Depends(get_db)):
    return JSONResponse(
        content={
            "message": "Lista de médicos por especialidad obtenida correctamente",
            "response": jsonable_encoder(service.obtener_medicos_por_especialidad(db, especialidad_id))
        },
        status_code=status.HTTP_200_OK
    )
