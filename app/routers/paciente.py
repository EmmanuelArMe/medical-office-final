from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.paciente import PacienteCreate, PacienteResponse
from app.services import paciente as service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/pacientes", response_model=PacienteResponse)
def crear_paciente(paciente: PacienteCreate, db: Session = Depends(get_db)):
    nuevo_paciente = service.crear_paciente(db, paciente)
    return JSONResponse(
        content={
            "message": "Paciente creado correctamente", "response": jsonable_encoder(nuevo_paciente)},
            status_code=status.HTTP_201_CREATED
    )

@router.get("/pacientes/{documento}", response_model=PacienteResponse)
def obtener_paciente_por_documento(documento: int, db: Session = Depends(get_db)):
    paciente = service.obtener_paciente_por_documento(db, documento=documento)
    return JSONResponse(
        content={
            "message": "Paciente obtenido correctamente", "response": jsonable_encoder(paciente)}, 
            status_code=status.HTTP_200_OK
    )

@router.get("/pacientes", response_model=list[PacienteResponse])
def obtener_pacientes(skip: int, limit: int, db: Session = Depends(get_db)):
    return JSONResponse( 
        content={"message": "Lista de pacientes obtenida correctamente", "response": jsonable_encoder(service.obtener_pacientes(db, skip, limit))},
        status_code=status.HTTP_200_OK
    )

@router.delete("/pacientes/{documento}", response_model=PacienteResponse)
def eliminar_paciente(documento: int, db: Session = Depends(get_db)):
    service.eliminar_paciente(db, documento=documento)
    return JSONResponse(
        content={
            "message": f"El paciente con el documento {documento} fue eliminado correctamente."
        },
        status_code=status.HTTP_200_OK
    )

@router.put("/pacientes/{documento}", response_model=PacienteResponse)
def actualizar_paciente(documento: int, paciente: PacienteCreate, db: Session = Depends(get_db)):
    paciente_actualizado = service.actualizar_paciente(db, documento, paciente)
    return JSONResponse(
        content={
            "message": f"Paciente con el documento {documento} actualizado correctamente",
            "response": jsonable_encoder(paciente_actualizado)
        },
        status_code=status.HTTP_200_OK
    )
