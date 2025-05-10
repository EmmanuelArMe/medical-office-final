from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.diagnostico import DiagnosticoCreate, DiagnosticoResponse
from app.services import diagnostico as diagnostico_service
from fastapi.encoders import jsonable_encoder

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/diagnosticos", response_model=DiagnosticoResponse)
def crear_diagnostico(diagnostico: DiagnosticoCreate, db: Session = Depends(get_db)):
    creado = diagnostico_service.crear_diagnostico(db, diagnostico)
    return JSONResponse(
        content={
            "message": "Diagnóstico creado correctamente",
            "response": jsonable_encoder(creado)
        },
        status_code=status.HTTP_201_CREATED
    )

@router.get("/diagnosticos", response_model=list[DiagnosticoResponse])
def listar_diagnosticos(db: Session = Depends(get_db)):
    return diagnostico_service.listar_diagnosticos(db)

@router.get("/diagnosticos/{diagnostico_id}", response_model=DiagnosticoResponse)
def obtener_diagnostico(diagnostico_id: int, db: Session = Depends(get_db)):
    diagnostico = diagnostico_service.obtener_diagnostico(db, diagnostico_id)
    if not diagnostico:
        return JSONResponse(
            content={"message": "Diagnóstico no encontrado"},
            status_code=status.HTTP_404_NOT_FOUND
        )
    return diagnostico

@router.delete("/diagnosticos/{diagnostico_id}", response_model=DiagnosticoResponse)
def eliminar_diagnostico(diagnostico_id: int, db: Session = Depends(get_db)):
    diagnostico = diagnostico_service.eliminar_diagnostico(db, diagnostico_id)
    if not diagnostico:
        return JSONResponse(
            content={"message": "Diagnóstico no encontrado"},
            status_code=status.HTTP_404_NOT_FOUND
        )
    return JSONResponse(
        content={
            "message": "Diagnóstico eliminado correctamente",
            "response": jsonable_encoder(diagnostico)
        },
        status_code=status.HTTP_200_OK
    )
