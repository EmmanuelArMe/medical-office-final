from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.diagnostico import DiagnosticoCreate, DiagnosticoResponse
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

@router.post("/diagnosticos", response_model=DiagnosticoResponse)
def crear_diagnostico(diagnostico: DiagnosticoCreate, db: Session = Depends(get_db)):
    nuevo_diagnostico = service.crear_diagnostico(db, diagnostico)
    return JSONResponse(
        content={"message": "Diagnóstico creado correctamente", "response": jsonable_encoder(nuevo_diagnostico)},
        status_code=status.HTTP_201_CREATED
    )

@router.get("/diagnosticos", response_model=list[DiagnosticoResponse])
def obtener_diagnosticos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    diagnosticos = service.obtener_diagnosticos(db, skip, limit)
    return JSONResponse(
        content={"message": "Lista de diagnósticos obtenida correctamente", "response": jsonable_encoder(diagnosticos)},
        status_code=status.HTTP_200_OK
    )

@router.get("/diagnosticos/{diagnostico_id}", response_model=DiagnosticoResponse)
def obtener_diagnostico(diagnostico_id: int, db: Session = Depends(get_db)):
    diagnostico = diagnostico_service.obtener_diagnostico(db, diagnostico_id)
    if not diagnostico:
        return JSONResponse(
            content={"message": "Diagnóstico no encontrado"},
            status_code=status.HTTP_404_NOT_FOUND
        )
    

@router.delete("/diagnosticos/{diagnostico_id}", response_model=DiagnosticoResponse)
def eliminar_diagnostico(diagnostico_id: int, db: Session = Depends(get_db)):
    diagnostico = diagnostico_service.eliminar_diagnostico(db, diagnostico_id)
    if not diagnostico:
        return JSONResponse(
            content={"message": f"Diagnóstico con ID {diagnostico_id} no encontrado"},
            status_code=status.HTTP_404_NOT_FOUND
        )
    return JSONResponse(
        content={"message": f"Diagnóstico con ID {diagnostico_id} eliminado correctamente", "response": jsonable_encoder(diagnostico)},
        status_code=status.HTTP_200_OK
    )