from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.paciente import PacienteCreate, PacienteResponse, PacienteUpdate
from app.services import paciente as service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
        "/pacientes",
        response_model=PacienteResponse,
        summary="Crear paciente",
        description="Crea un nuevo paciente en el sistema."
)
def crear_paciente(paciente: PacienteCreate, db: Session = Depends(get_db)):
    nuevo_paciente = service.crear_paciente(db, paciente)
    return JSONResponse(
        content={
            "message": "Paciente creado correctamente", "response": jsonable_encoder(nuevo_paciente)},
            status_code=status.HTTP_201_CREATED
    )

@router.get(
        "/pacientes/{documento}",
        response_model=PacienteResponse,
        summary="Obtener paciente por documento",
        description="Obtiene un paciente por su documento de identidad."
)
def obtener_paciente_por_documento(documento: int, db: Session = Depends(get_db)):
    paciente = service.obtener_paciente_por_documento(db, documento=documento)
    return JSONResponse(
        content={
            "message": "Paciente obtenido correctamente", "response": jsonable_encoder(paciente)}, 
            status_code=status.HTTP_200_OK
    )

@router.get(
        "/pacientes",
        response_model=list[PacienteResponse],
        summary="Obtener lista de pacientes",
        description="Obtiene una lista de pacientes paginada."
)
def obtener_pacientes(skip: int, limit: int, db: Session = Depends(get_db)):
    return JSONResponse( 
        content={"message": "Lista de pacientes obtenida correctamente", "response": jsonable_encoder(service.obtener_pacientes(db, skip, limit))},
        status_code=status.HTTP_200_OK
    )

@router.delete(
        "/pacientes/{documento}",
        response_model=PacienteResponse,
        summary="Eliminar paciente",
        description="Elimina un paciente por su documento de identidad."
)
def eliminar_paciente(documento: int, db: Session = Depends(get_db)):
    paciente = service.eliminar_paciente(db, documento=documento)
    return JSONResponse(
        content={"message": f"El paciente con el documento {documento} fue eliminado correctamente.", "response": jsonable_encoder(paciente)},
        status_code=status.HTTP_200_OK
    )

@router.put(
        "/pacientes/{documento}",
        response_model=PacienteResponse,
        summary="Actualizar paciente",
        description="Actualiza un paciente por su documento de identidad."
)
def actualizar_paciente(documento: int, paciente: PacienteUpdate, db: Session = Depends(get_db)):
    paciente_actualizado = service.actualizar_paciente(db, documento, paciente)
    return JSONResponse(
        content={
            "message": f"Paciente con el documento {documento} actualizado correctamente",
            "response": jsonable_encoder(paciente_actualizado)
        },
        status_code=status.HTTP_200_OK
    )
