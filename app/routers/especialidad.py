from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.especialidad import EspecialidadCreate, EspecialidadResponse, EspecialidadUpdate
from app.services import especialidad as service
from fastapi.encoders import jsonable_encoder

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
        "/especialidades",
        response_model=EspecialidadResponse,
        summary="Crear especialidad",
        description="Crea una nueva especialidad en el sistema."
)
def crear_especialidad(especialidad: EspecialidadCreate, db: Session = Depends(get_db)):
    nueva_especialidad = service.crear_especialidad(db, especialidad)
    return JSONResponse(
        content={"message": "Especialidad creada correctamente", "response": jsonable_encoder(nueva_especialidad)},
        status_code=status.HTTP_201_CREATED
    )

@router.get(
        "/especialidades/{especialidad_id}",
        response_model=EspecialidadResponse,
        summary="Obtener especialidad por ID",
        description="Obtiene una especialidad por su ID."
)
def obtener_especialidad_por_id(especialidad_id: int, db: Session = Depends(get_db)):
    especialidad = service.obtener_especialidad_por_id(db, especialidad_id)
    return JSONResponse(
        content={"message": "Especialidad obtenida correctamente", "response": jsonable_encoder(especialidad)},
        status_code=status.HTTP_200_OK
    )

@router.get(
        "/especialidades",
        response_model=list[EspecialidadResponse],
        summary="Obtener lista de especialidades",
        description="Obtiene una lista de especialidades paginada."
)
def obtener_especialidades(skip: int, limit: int, db: Session = Depends(get_db)):
    especialidades = service.obtener_especialidades(db, skip=skip, limit=limit)
    return JSONResponse(
        content={"message": "Lista de especialidades obtenida correctamente", "response": jsonable_encoder(especialidades)},
        status_code=status.HTTP_200_OK
    )

@router.delete(
        "/especialidades/{especialidad_id}",
        response_model=EspecialidadResponse,
        summary="Eliminar especialidad",
        description="Elimina una especialidad por su ID."
)
def eliminar_especialidad(especialidad_id: int, db: Session = Depends(get_db)):
    especialidad_eliminada = service.eliminar_especialidad(db, especialidad_id)
    return JSONResponse(
        content={"message": f"Especialidad con ID {especialidad_id} eliminada correctamente", "response": jsonable_encoder(especialidad_eliminada)},
        status_code=status.HTTP_200_OK
    )

@router.put(
        "/especialidades/{especialidad_id}",
        response_model=EspecialidadResponse,
        summary="Actualizar especialidad",
        description="Actualiza una especialidad por su ID."
)
def actualizar_especialidad(especialidad_id: int, especialidad: EspecialidadUpdate, db: Session = Depends(get_db)):
    especialidad_actualizada = service.actualizar_especialidad(db, especialidad_id, especialidad)
    return JSONResponse(
        content={"message": f"Especialidad con ID {especialidad_id} actualizada correctamente", "response": jsonable_encoder(especialidad_actualizada)},
        status_code=status.HTTP_200_OK
    )