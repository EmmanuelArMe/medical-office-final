from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.historial_medico import HistorialMedicoCreate, HistorialMedicoResponse, HistorialMedicoUpdate
from app.services import historial_medico as service
from fastapi.responses import JSONResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
        "/historiales",
        response_model=HistorialMedicoResponse,
        summary="Crear historial médico",
        description="Crea un nuevo historial médico en el sistema."
)
def crear_historial_medico(historial: HistorialMedicoCreate, db: Session = Depends(get_db)):
    nuevo_historial_medico = service.crear_historial_medico(db, historial)
    return JSONResponse(
        content={
            "message": "Historial médico creado correctamente",
            "response": jsonable_encoder(nuevo_historial_medico)
        },
        status_code=status.HTTP_201_CREATED
    )

@router.get(
        "/historiales/{id}",
        response_model=HistorialMedicoResponse,
        summary="Obtener historial médico por ID",
        description="Obtiene un historial médico por su ID."
)
def obtener_historial_medico_por_id(id: int, db: Session = Depends(get_db)):
    historial_medico = service.obtener_historial_medico_por_id(db, id)
    return JSONResponse(
        content={
            "message": "Historial médico obtenido correctamente",
            "response": jsonable_encoder(historial_medico)
        },
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/historiales",
        response_model=list[HistorialMedicoResponse],
        summary="Obtener lista de historiales médicos",
        description="Obtiene una lista de historiales médicos paginada."
)
def obtener_historiales_medicos(skip: int, limit: int, db: Session = Depends(get_db)):
    return JSONResponse(
        content={
            "message": "Lista de historiales médicos obtenidos correctamente",
            "response": jsonable_encoder(service.obtener_historiales_medicos(db, skip, limit))
        },
        status_code=status.HTTP_200_OK
    )

@router.delete(
        "/historiales/{id}",
        response_model=HistorialMedicoResponse,
        summary="Eliminar historial médico",
        description="Elimina un historial médico por su ID."
)
def eliminar_historial_medico(id: int, db: Session = Depends(get_db)):
    historial_medico = service.eliminar_historial_medico(db, id)
    return JSONResponse(
        content={
            "message": "Historial médico eliminado correctamente",
            "response": jsonable_encoder(historial_medico)
        }, 
        status_code=status.HTTP_200_OK
    )

@router.put(
        "/historiales/{id}",
        response_model=HistorialMedicoResponse,
        summary="Actualizar historial médico",
        description="Actualiza un historial médico por su ID."
)
def actualizar_historial_medico(id: int, historial: HistorialMedicoUpdate, db: Session = Depends(get_db)):
    historial_medico_actualizado = service.actualizar_historial_medico(db, id, historial)
    if historial_medico_actualizado:
        return JSONResponse(
            content={
                "message": f"Historial médico con el id {id} ha sido actualizado correctamente",
                "response": jsonable_encoder(historial_medico_actualizado)
            },
            status_code=status.HTTP_200_OK
        )

@router.get(
        "/historiales/paciente/{id}",
        response_model=list[HistorialMedicoResponse],
        summary="Obtener historiales médicos por ID de paciente",
        description="Obtiene una lista de historiales médicos por el ID del paciente."
)
def obtener_historiales_medicos_por_id_paciente(id: int, db: Session = Depends(get_db)):
    historial_medico = service.obtener_historiales_medicos_por_id_paciente(db, id)
    return JSONResponse(
        content={
            "message": f"Lista de historiales médicos del paciente con id {id}, obtenidos correctamente",
            "response": jsonable_encoder(historial_medico)
        },
        status_code=status.HTTP_200_OK
    )