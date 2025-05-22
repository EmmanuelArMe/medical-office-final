from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.db.database import get_db # Corrected import
from app.schemas.diagnostico import DiagnosticoCreate, DiagnosticoResponse, DiagnosticoUpdate
from app.services import diagnostico as service # Consolidated service import
# from app.services import diagnostico as diagnostico_service # Redundant, use 'service'
from app.utils.auth import get_current_user
from app.models.usuario import Usuario # For type hinting current_user

router = APIRouter()

# Removed local get_db definition

@router.post(
        "/diagnosticos",
        response_model=DiagnosticoResponse,
        summary="Crear diagnóstico",
        description="Crea un nuevo diagnóstico en el sistema."
)
def crear_diagnostico(diagnostico: DiagnosticoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    nuevo_diagnostico = service.crear_diagnostico(db, diagnostico)
    return JSONResponse(
        content={"message": "Diagnóstico creado correctamente", "response": jsonable_encoder(nuevo_diagnostico)},
        status_code=status.HTTP_201_CREATED
    )

@router.get(
        "/diagnosticos/{id}",
        response_model=DiagnosticoResponse,
        summary="Obtener diagnóstico por ID",
        description="Obtiene un diagnóstico por su ID."
)
def obtener_diagnostico_por_id(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    diagnostico = service.obtener_diagnostico_por_id(db, id) # Use consolidated 'service'
    return JSONResponse(
        content={"message": "Diagnóstico obtenido correctamente", "response": jsonable_encoder(diagnostico)},
        status_code=status.HTTP_200_OK
    )
    
@router.get(
        "/diagnosticos",
        response_model=list[DiagnosticoResponse],
        summary="Obtener lista de diagnósticos",
        description="Obtiene una lista de diagnósticos paginada."
)
def obtener_diagnosticos(skip: int, limit: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    diagnosticos = service.obtener_diagnosticos(db, skip, limit)
    return JSONResponse(
        content={"message": "Lista de diagnósticos obtenida correctamente", "response": jsonable_encoder(diagnosticos)},
        status_code=status.HTTP_200_OK
    )

@router.delete(
        "/diagnosticos/{id}",
        response_model=DiagnosticoResponse,
        summary="Eliminar diagnóstico",
        description="Elimina un diagnóstico por su ID."
)
def eliminar_diagnostico(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    diagnostico = service.eliminar_diagnostico(db, id) # Use consolidated 'service'
    return JSONResponse(
        content={"message": f"Diagnóstico con ID {id} eliminado correctamente", "response": jsonable_encoder(diagnostico)},
        status_code=status.HTTP_200_OK
    )

@router.put(
        "/diagnostico/{id}",
        response_model=DiagnosticoResponse,
        summary="Actualizar diagnóstico",
        description="Actualiza un diagnóstico por su ID."
)
def actualizar_diagnostico(id: int, diagnostico: DiagnosticoUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    diagnostico_actualizado = service.actualizar_diagnostico(db, id, diagnostico)
    return JSONResponse(
        content={
            "message": f"Consultorio con ID {id} actualizado correctamente", # Typo: Should be "Diagnóstico"
            "response": jsonable_encoder(diagnostico_actualizado)
        }
    )

@router.get(
        "/diagnosticos/citas/{id}",
        response_model=list[DiagnosticoResponse],
        summary="Obtener diagnósticos por cita",
        description="Obtiene una lista de diagnósticos asociados a una cita."
)
def obtener_diagnosticos_por_cita(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    diagnosticos = service.obtener_diagnosticos_por_cita(db, id)
    return JSONResponse(
        content={"message": "Lista de diagnósticos obtenida correctamente", "response": jsonable_encoder(diagnosticos)},
        status_code=status.HTTP_200_OK
    )
