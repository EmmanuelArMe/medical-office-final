from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.medico import MedicoCreate, MedicoResponse
from app.services import medico as service
from fastapi.encoders import jsonable_encoder

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/medicos", response_model=MedicoResponse)
def crear_medico(medico: MedicoCreate, db: Session = Depends(get_db)):
    nuevo_medico = service.registrar_medico(db, medico)
    return JSONResponse(
        content={
            "message": "Médico creado correctamente",
            "response": jsonable_encoder(nuevo_medico)
        },
        status_code=status.HTTP_201_CREATED
    )

@router.get("/medicos", response_model=list[MedicoResponse])
def listar_medicos(db: Session = Depends(get_db)):
    return service.listar_medicos(db)

@router.get("/medicos/{medico_id}", response_model=MedicoResponse)
def obtener_medico(medico_id: int, db: Session = Depends(get_db)):
    medico = service.obtener_medico(db, medico_id)
    if not medico:
        return JSONResponse(
            content={"message": "Médico no encontrado"},
            status_code=status.HTTP_404_NOT_FOUND
        )
    return medico

@router.delete("/medicos/{medico_id}", response_model=MedicoResponse)
def eliminar_medico(medico_id: int, db: Session = Depends(get_db)):
    medico = service.eliminar_medico(db, medico_id)
    if not medico:
        return JSONResponse(
            content={"message": "Médico no encontrado"},
            status_code=status.HTTP_404_NOT_FOUND
        )
    return JSONResponse(
        content={
            "message": "Médico eliminado correctamente",
            "response": jsonable_encoder(medico)
        },
        status_code=status.HTTP_200_OK
    )
