from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.diagnostico import DiagnosticoCreate, DiagnosticoResponse, DiagnosticoUpdate
from app.services import diagnostico as diagnostico_service
from fastapi.encoders import jsonable_encoder
from app.services import diagnostico as service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
        "/diagnosticos",
        response_model=DiagnosticoResponse,
        summary="Crear diagnóstico",
        description="Crea un nuevo diagnóstico en el sistema."
)
def crear_diagnostico(diagnostico: DiagnosticoCreate, db: Session = Depends(get_db)):
    nuevo_diagnostico = service.crear_diagnostico(db, diagnostico)
    return JSONResponse(
        content={"message": "Diagnóstico creado correctamente", "response": jsonable_encoder(nuevo_diagnostico)},
        status_code=status.HTTP_201_CREATED
    )

@router.get(
        "/diagnosticos/{diagnostico_id}",
        response_model=DiagnosticoResponse,
        summary="Obtener diagnóstico por ID",
        description="Obtiene un diagnóstico por su ID."
)
def obtener_diagnostico_por_id(diagnostico_id: int, db: Session = Depends(get_db)):
    diagnostico = diagnostico_service.obtener_diagnostico_por_id(db, diagnostico_id)
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
def obtener_diagnosticos(skip: int, limit: int, db: Session = Depends(get_db)):
    diagnosticos = service.obtener_diagnosticos(db, skip, limit)
    return JSONResponse(
        content={"message": "Lista de diagnósticos obtenida correctamente", "response": jsonable_encoder(diagnosticos)},
        status_code=status.HTTP_200_OK
    )

@router.delete(
        "/diagnosticos/{diagnostico_id}",
        response_model=DiagnosticoResponse,
        summary="Eliminar diagnóstico",
        description="Elimina un diagnóstico por su ID."
)
def eliminar_diagnostico(diagnostico_id: int, db: Session = Depends(get_db)):
    diagnostico = diagnostico_service.eliminar_diagnostico(db, diagnostico_id)
    return JSONResponse(
        content={"message": f"Diagnóstico con ID {diagnostico_id} eliminado correctamente", "response": jsonable_encoder(diagnostico)},
        status_code=status.HTTP_200_OK
    )

@router.put(
        "/diagnostico/{diagnostico_id}",
        response_model=DiagnosticoResponse,
        summary="Actualizar diagnóstico",
        description="Actualiza un diagnóstico por su ID."
)
def actualizar_diagnostico(diagnostico_id: int, diagnostico: DiagnosticoUpdate, db: Session = Depends(get_db)):
    diagnostico_actualizado = service.actualizar_diagnostico(db, diagnostico_id, diagnostico)
    return JSONResponse(
        content={
            "message": f"Consultorio con ID {diagnostico_id} actualizado correctamente",
            "response": jsonable_encoder(diagnostico_actualizado)
        }
    )

@router.get(
        "/diagnosticos/citas/{cita_id}",
        response_model=list[DiagnosticoResponse],
        summary="Obtener diagnósticos por cita",
        description="Obtiene una lista de diagnósticos asociados a una cita."
)
def obtener_diagnosticos_por_cita(cita_id: int, db: Session = Depends(get_db)):
    diagnosticos = service.obtener_diagnosticos_por_cita(db, cita_id)
    return JSONResponse(
        content={"message": "Lista de diagnósticos obtenida correctamente", "response": jsonable_encoder(diagnosticos)},
        status_code=status.HTTP_200_OK
    )
